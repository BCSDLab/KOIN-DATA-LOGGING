import json
import re
import time
import urllib.error
import urllib.request


class IncompleteSource(RuntimeError):
    pass


def text_of(rich_text):
    return ''.join(x.get('plain_text', x.get('text', {}).get('content', '')) for x in rich_text)


class NotionSource:
    def __init__(self, token, root, request=None, sleep=time.sleep):
        self.token, self.root = token, root.replace('-', '')
        self.request_override, self.sleep = request, sleep
        self.visited, self.databases, self.rows, self.pages = set(), {}, {}, []

    def request(self, path, payload=None):
        if self.request_override:
            return self.request_override(path, payload)
        for attempt in range(6):
            req = urllib.request.Request('https://api.notion.com/v1/' + path,
                  data=json.dumps(payload).encode() if payload is not None else None,
                  headers={'Authorization': 'Bearer ' + self.token, 'Notion-Version': '2025-09-03',
                           'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=40) as response:
                    return json.load(response)
            except urllib.error.HTTPError as exc:
                if exc.code in (429, 500, 502, 503, 504, 529) and attempt < 5:
                    self.sleep(min(120, max(float(exc.headers.get('Retry-After', 0)), 2 ** attempt)))
                    continue
                raise IncompleteSource('Notion HTTP ' + str(exc.code)) from None
            except (OSError, ValueError):
                if attempt < 5:
                    self.sleep(2 ** attempt)
                    continue
                raise IncompleteSource('Notion transport failed') from None
        raise IncompleteSource('Notion retry exhausted')

    def all_results(self, path, post=False):
        cursor = None
        seen = set()
        while True:
            payload = {'page_size': 100}
            if cursor:
                payload['start_cursor'] = cursor
            if post:
                response = self.request(path, payload)
            else:
                import urllib.parse
                response = self.request(path + '?' + urllib.parse.urlencode(payload))
            if 'results' not in response:
                raise IncompleteSource('Notion result list missing')
            yield from response['results']
            if not response.get('has_more'):
                break
            cursor = response.get('next_cursor')
            if not cursor or cursor in seen:
                raise IncompleteSource('Notion pagination incomplete')
            seen.add(cursor)

    def blocks(self, page_id):
        result = []
        for block in self.all_results('blocks/' + page_id + '/children'):
            if block.get('type') == 'unsupported':
                raise IncompleteSource('Unsupported Notion block')
            if block.get('has_children') and block['type'] not in ('child_page', 'child_database'):
                block['_children'] = self.blocks(block['id'])
            result.append(block)
        return result

    def render(self, blocks, depth=0):
        lines = []
        for block in blocks:
            kind = block['type']
            data = block.get(kind, {})
            prefix = '#' * int(kind[-1]) + ' ' if re.fullmatch(r'heading_[123]', kind) else '- ' if kind in ('bulleted_list_item', 'numbered_list_item') else ''
            lines.append('    ' * depth + prefix + text_of(data.get('rich_text', [])))
            lines.extend(self.render(block.get('_children', []), depth + 1))
        return lines

    def descendants(self, blocks):
        for b in blocks:
            yield b
            yield from self.descendants(b.get('_children', []))

    def page_title(self, obj):
        return next((text_of(v.get('title', [])) for v in obj.get('properties', {}).values() if v.get('type') == 'title'), '')

    def database(self, database_id, service):
        database = self.request('databases/' + database_id)
        sources = database.get('data_sources')
        if sources is None:
            raise IncompleteSource('Database data_sources unavailable')
        for source in sources:
            source_id = source['id']
            if source_id in self.databases:
                continue
            # Fetch schema before querying. No saved-view filters are applied.
            self.request('data_sources/' + source_id)
            rows = list(self.all_results('data_sources/' + source_id + '/query', post=True))
            self.databases[source_id] = len(rows)
            for row in rows:
                if row.get('archived') or row.get('in_trash'):
                    continue
                self.rows[row['id'].replace('-', '')] = row
                self.page(row['id'], service, obj=row, is_row=True)

    def page(self, page_id, service='', obj=None, is_row=False, root=False):
        page_id = page_id.replace('-', '')
        if page_id in self.visited:
            return
        self.visited.add(page_id)
        obj = obj or self.request('pages/' + page_id)
        title = self.page_title(obj)
        if title.strip() == 'Event Log (과거)':
            return
        blocks = self.blocks(page_id)
        rendered = '\n'.join(self.render(blocks))
        props = obj.get('properties', {})
        platforms = [x['name'] for x in props.get('platform', {}).get('multi_select', [])]
        row = dict(id=page_id, url='https://www.notion.so/' + page_id, title=title, service=service,
                   platforms=platforms, text=rendered, edited=obj.get('last_edited_time'), is_row=is_row,
                   unresolved='forced_update' in rendered and ('__app_update__exit' in rendered or 'forced_update_exit' in rendered))
        if is_row:
            self.pages.append(row)
        for b in self.descendants(blocks):
            kind, body = b['type'], b.get(b['type'], {})
            if kind == 'child_database':
                self.database(b['id'], service or title)
            elif kind == 'child_page':
                self.page(b['id'], service or body.get('title', title))
            elif kind == 'link_to_page':
                if body.get('type') == 'page_id':
                    self.page(body['page_id'], service or title)
                elif body.get('type') == 'database_id':
                    self.database(body['database_id'], service or title)
            # Only root's service navigation links are traversed. Cross-references
            # inside contracts must not change ownership or pull unrelated workspaces.
            if root:
                for rt in body.get('rich_text', []):
                    url = rt.get('href') or (rt.get('text', {}).get('link') or {}).get('url', '')
                    if re.match(r'https://(?:www\.)?(?:app\.)?notion\.(?:so|com)/', url or ''):
                        m = re.search(r'([a-f0-9]{32}|[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12})(?:[?/#]|$)', url)
                        if m:
                            name = rt.get('plain_text') or rt.get('text', {}).get('content', '')
                            self.page(m.group(1), name)
                    if rt.get('type') == 'mention' and rt.get('mention', {}).get('type') == 'page':
                        self.page(rt['mention']['page']['id'], rt.get('plain_text', ''))

    def collect(self):
        self.page(self.root, root=True)
        if not self.databases or not self.pages:
            raise IncompleteSource('No data sources or logging pages discovered')
        return dict(pages=self.pages, databases=self.databases, row_count=len(self.rows),
                    complete=True, root=self.root)
