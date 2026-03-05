/**
 * 咒语数据库
 * 定义音节到元素/形态/修饰的映射表（v0.1 占位版，后续可调整）
 */

export type Element = 'fire' | 'ice' | 'thunder' | 'earth';
export type Form = 'bolt' | 'burst' | 'shield' | 'blade' | 'zone' | 'heal';
export type Modifier = 'power' | 'chain' | 'pierce' | 'delay' | 'scatter' | 'track';

export type SlotType = Element | Form | Modifier;

/** 音节映射表 */
export const SYLLABLE_MAP: Record<string, SlotType> = {
  // 元素
  'a': 'fire',   'ah': 'fire',
  'i': 'ice',    'ee': 'ice',
  'u': 'thunder','oo': 'thunder',
  'e': 'earth',  'eh': 'earth',

  // 形态
  'ka': 'bolt',    'ta': 'bolt',
  'bo': 'burst',   'po': 'burst',
  'shi': 'shield', 'si': 'shield',
  'ra': 'blade',   'la': 'blade',
  'yu': 'zone',    'wu': 'zone',
  'mi': 'heal',    'ni': 'heal',

  // 修饰
  'da': 'power',   'ga': 'power',
  're': 'chain',   'le': 'chain',
  'su': 'pierce',  'fu': 'pierce',
  'chi': 'delay',  'zi': 'delay',
  'sa': 'scatter', 'ha': 'scatter',
  'to': 'track',   'do': 'track',
};

export const ELEMENT_LABELS: Record<Element, string> = {
  fire: '火',
  ice: '冰',
  thunder: '雷',
  earth: '土',
};

export const FORM_LABELS: Record<Form, string> = {
  bolt: '弹',
  burst: '爆',
  shield: '盾',
  blade: '刃',
  zone: '域',
  heal: '愈',
};

export const MODIFIER_LABELS: Record<Modifier, string> = {
  power: '强',
  chain: '连',
  pierce: '穿',
  delay: '迟',
  scatter: '散',
  track: '追',
};

export function isElement(s: SlotType): s is Element {
  return ['fire', 'ice', 'thunder', 'earth'].includes(s);
}

export function isForm(s: SlotType): s is Form {
  return ['bolt', 'burst', 'shield', 'blade', 'zone', 'heal'].includes(s);
}

export function isModifier(s: SlotType): s is Modifier {
  return ['power', 'chain', 'pierce', 'delay', 'scatter', 'track'].includes(s);
}
