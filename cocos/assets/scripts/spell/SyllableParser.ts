import { SYLLABLE_MAP, SlotType } from './SpellDatabase';

/**
 * 将语音识别的原始文本解析为音节列表（最多3个）
 * 当前策略：按空格/标点分词，逐词查映射表
 * 未匹配的词会被忽略（后续可以加"发现"提示）
 */
export function parseSyllables(raw: string): string[] {
  const tokens = raw
    .toLowerCase()
    .replace(/[^a-z\u4e00-\u9fa5\s]/g, ' ')
    .split(/\s+/)
    .filter(t => t.length > 0);

  const matched: string[] = [];
  for (const token of tokens) {
    if (SYLLABLE_MAP[token] !== undefined) {
      matched.push(token);
      if (matched.length >= 3) break;
    }
  }
  return matched;
}

/**
 * 将音节列表映射为属性列表
 */
export function mapSyllablesToSlots(syllables: string[]): SlotType[] {
  return syllables
    .map(s => SYLLABLE_MAP[s])
    .filter((v): v is SlotType => v !== undefined);
}
