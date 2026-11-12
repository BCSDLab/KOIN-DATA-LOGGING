export type Platform = 'WEB' | 'WEB (모바일)' | 'ANDROID' | 'IOS';
export type ContractStatus = 'approved' | 'draft' | 'legacy' | 'frozen';
export type SupportState = 'confirmed' | 'unsupported' | 'unknown';
export type WireValue = string | number | boolean;

export interface ValueDescriptor {
  type: 'string' | 'number' | 'boolean';
  description: string;
  required: boolean;
  enum?: WireValue[];
  const?: WireValue;
}

export interface PlatformSupport {
  state: SupportState;
  evidence: string;
}

export interface ContractEvent {
  description: string;
  event_name: string;
  event_label: string;
  event_category: string;
  value: ValueDescriptor;
  params: Record<string, ValueDescriptor>;
  platforms: Platform[];
  status: ContractStatus;
  source: string;
  decision?: string;
  notes?: string;
  platform_support: Record<Platform, PlatformSupport>;
}

export interface SpecData {
  schema_version: 1;
  service: string;
  screen_view: string;
  events: ContractEvent[];
}

export interface ScreenOverride {
  service: string;
  screen_view: string;
  event_name: string;
  reason: string;
}

export interface Vocabulary {
  schema_version: 1;
  categories: string[];
  platforms: Platform[];
  services: Record<string, string>;
  screen_overrides: ScreenOverride[];
}

export interface Envelope {
  schema_version: 1;
  reserved_keys: string[];
  notes: string;
}

export interface CanonicalModel {
  vocabulary: Vocabulary;
  envelope: Envelope;
  specs: Array<{ file: string; data: SpecData }>;
}

export type Model = CanonicalModel;
export type SelectedEvent = ContractEvent & Pick<SpecData, 'service' | 'screen_view'>;

export function validate(model: CanonicalModel): string[];
export function events(model: CanonicalModel, preview?: boolean): SelectedEvent[];
export function generate(model: CanonicalModel, options?: { preview?: boolean }): Record<string, string>;
