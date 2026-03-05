import { VoiceEngine, VoiceResult } from './VoiceEngine';
import { parseSyllables } from '../spell/SyllableParser';

/**
 * 微信小游戏语音引擎
 * 使用 wx.startRecord 录音 + 腾讯云 ASR 识别
 * TODO: 接入实际 ASR 服务时替换 uploadAndRecognize 实现
 */
export class WxSpeechEngine implements VoiceEngine {
  onResult: ((result: VoiceResult) => void) | null = null;
  onError: ((error: string) => void) | null = null;

  private listening = false;
  private tempFilePath = '';

  start(): void {
    this.listening = true;
    // @ts-ignore
    wx.startRecord({
      success: () => {},
      fail: (err: any) => {
        this.listening = false;
        this.onError?.(JSON.stringify(err));
      },
    });
  }

  stop(): void {
    if (!this.listening) return;
    this.listening = false;
    // @ts-ignore
    wx.stopRecord({
      success: (res: any) => {
        this.tempFilePath = res.tempFilePath;
        this.uploadAndRecognize(res.tempFilePath);
      },
      fail: (err: any) => {
        this.onError?.(JSON.stringify(err));
      },
    });
  }

  isListening(): boolean {
    return this.listening;
  }

  /**
   * 上传录音文件并调用 ASR 识别
   * TODO: 替换为实际的腾讯云/科大讯飞 ASR 接口
   */
  private uploadAndRecognize(filePath: string): void {
    console.log('[WxSpeechEngine] TODO: upload and recognize', filePath);
    // 占位：模拟返回一个识别结果
    const raw = 'a';
    const syllables = parseSyllables(raw);
    this.onResult?.({ raw, syllables, confidence: 1.0 });
  }
}
