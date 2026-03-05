import { VoiceEngine, VoiceResult } from './VoiceEngine';
import { parseSyllables } from '../spell/SyllableParser';

/**
 * Web 平台语音引擎
 * 使用浏览器原生 Web Speech API
 * Chrome 支持最好，需要 HTTPS 或 localhost
 */
export class WebSpeechEngine implements VoiceEngine {
  onResult: ((result: VoiceResult) => void) | null = null;
  onError: ((error: string) => void) | null = null;

  private recognition: any = null;
  private listening = false;

  constructor() {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      console.warn('[WebSpeechEngine] Web Speech API not supported');
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.lang = 'zh-CN';
    this.recognition.interimResults = false;
    this.recognition.maxAlternatives = 1;

    this.recognition.onresult = (event: any) => {
      const raw: string = event.results[0][0].transcript;
      const confidence: number = event.results[0][0].confidence;
      const syllables = parseSyllables(raw);
      this.onResult?.({ raw, syllables, confidence });
    };

    this.recognition.onerror = (event: any) => {
      this.listening = false;
      this.onError?.(event.error);
    };

    this.recognition.onend = () => {
      this.listening = false;
    };
  }

  start(): void {
    if (!this.recognition) {
      this.onError?.('Web Speech API not supported');
      return;
    }
    this.listening = true;
    this.recognition.start();
  }

  stop(): void {
    if (this.recognition && this.listening) {
      this.recognition.stop();
    }
    this.listening = false;
  }

  isListening(): boolean {
    return this.listening;
  }
}
