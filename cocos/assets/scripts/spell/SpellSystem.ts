import { _decorator, Component, EventTarget } from 'cc';
import { VoiceResult } from '../voice/VoiceEngine';
import { mapSyllablesToSlots } from './SyllableParser';
import {
  Element, Form, Modifier,
  isElement, isForm, isModifier,
  ELEMENT_LABELS, FORM_LABELS, MODIFIER_LABELS,
} from './SpellDatabase';

const { ccclass } = _decorator;

export interface SpellCast {
  element: Element;
  form: Form | null;
  modifier: Modifier | null;
  /** 咒语等级：1=仅元素, 2=元素+形态, 3=元素+形态+修饰 */
  level: 1 | 2 | 3;
  /** 人类可读描述，如「强火球」 */
  label: string;
}

/** 咒语解析完成事件 */
export const EVENT_SPELL_CAST = 'spell-cast';
/** 识别到未知音节事件（用于 A2 提示系统） */
export const EVENT_UNKNOWN_SYLLABLE = 'unknown-syllable';

@ccclass('SpellSystem')
export class SpellSystem extends Component {
  /** 供外部监听咒语事件 */
  readonly events = new EventTarget();

  /**
   * 接收语音识别结果，解析并广播咒语
   */
  handleVoiceResult(result: VoiceResult): void {
    const slots = mapSyllablesToSlots(result.syllables);

    // 提取各槽位（以第一个匹配到对应类型的为准）
    const element = slots.find(isElement) as Element | undefined;
    const form = slots.find(isForm) as Form | undefined;
    const modifier = slots.find(isModifier) as Modifier | undefined;

    // 元素是必须的
    if (!element) {
      this.events.emit(EVENT_UNKNOWN_SYLLABLE, result.raw);
      return;
    }

    const level: 1 | 2 | 3 = modifier ? 3 : form ? 2 : 1;
    const label = this.buildLabel(element, form ?? null, modifier ?? null);

    const spell: SpellCast = {
      element,
      form: form ?? null,
      modifier: modifier ?? null,
      level,
      label,
    };

    this.events.emit(EVENT_SPELL_CAST, spell);
  }

  private buildLabel(element: Element, form: Form | null, modifier: Modifier | null): string {
    const parts = [
      modifier ? MODIFIER_LABELS[modifier] : '',
      ELEMENT_LABELS[element],
      form ? FORM_LABELS[form] : '',
    ];
    return parts.join('');
  }
}
