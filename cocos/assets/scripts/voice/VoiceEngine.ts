/**
 * 语音引擎抽象接口
 * 不同平台（Web / 微信小游戏）实现此接口，游戏逻辑只依赖此接口
 */
export interface VoiceResult {
  /** 识别到的原始文本 */
  raw: string;
  /** 解析出的音节列表，最多3个 */
  syllables: string[];
  /** 置信度 0~1 */
  confidence: number;
}

export interface VoiceEngine {
  /** 开始录音/识别 */
  start(): void;
  /** 停止录音/识别 */
  stop(): void;
  /** 是否正在监听 */
  isListening(): boolean;
  /** 识别完成回调 */
  onResult: ((result: VoiceResult) => void) | null;
  /** 识别出错回调 */
  onError: ((error: string) => void) | null;
}

/** 工厂方法：根据当前平台返回对应引擎 */
export function createVoiceEngine(): VoiceEngine {
  // @ts-ignore
  if (typeof wx !== 'undefined' && wx.startRecord) {
    const { WxSpeechEngine } = require('./WxSpeechEngine');
    return new WxSpeechEngine();
  }
  const { WebSpeechEngine } = require('./WebSpeechEngine');
  return new WebSpeechEngine();
}
