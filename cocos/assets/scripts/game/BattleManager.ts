import { _decorator, Component, Node, director } from 'cc';
import { createVoiceEngine, VoiceEngine } from '../voice/VoiceEngine';
import { SpellSystem, SpellCast, EVENT_SPELL_CAST, EVENT_UNKNOWN_SYLLABLE } from '../spell/SpellSystem';
import { FocusSystem } from './FocusSystem';
import { Character } from './Character';

const { ccclass, property } = _decorator;

export type BattleState = 'idle' | 'casting' | 'paused' | 'gameover';

/**
 * 战斗管理器
 * 负责协调：时停机制、语音识别触发、咒语派发、战斗状态机
 */
@ccclass('BattleManager')
export class BattleManager extends Component {
  @property(Node) characterNode: Node | null = null;
  @property(Node) spellSystemNode: Node | null = null;
  @property(Node) focusSystemNode: Node | null = null;

  private voiceEngine: VoiceEngine | null = null;
  private spellSystem: SpellSystem | null = null;
  private focusSystem: FocusSystem | null = null;
  private character: Character | null = null;

  private state: BattleState = 'idle';
  /** 时停时的时间缩放（0 = 完全暂停） */
  private readonly CAST_TIME_SCALE = 0;

  onLoad(): void {
    this.spellSystem = this.spellSystemNode?.getComponent(SpellSystem) ?? null;
    this.focusSystem = this.focusSystemNode?.getComponent(FocusSystem) ?? null;
    this.character = this.characterNode?.getComponent(Character) ?? null;

    this.voiceEngine = createVoiceEngine();
    this.voiceEngine.onResult = (result) => {
      this.spellSystem?.handleVoiceResult(result);
      this.endCast();
    };
    this.voiceEngine.onError = (err) => {
      console.warn('[BattleManager] voice error:', err);
      this.endCast();
    };

    this.spellSystem?.events.on(EVENT_SPELL_CAST, this.onSpellCast, this);
    this.spellSystem?.events.on(EVENT_UNKNOWN_SYLLABLE, this.onUnknownSyllable, this);
  }

  onDestroy(): void {
    this.voiceEngine?.stop();
    this.spellSystem?.events.off(EVENT_SPELL_CAST, this.onSpellCast, this);
    this.spellSystem?.events.off(EVENT_UNKNOWN_SYLLABLE, this.onUnknownSyllable, this);
  }

  /** 玩家按下施法键：消耗 Focus，时停，开始监听 */
  startCast(): void {
    if (this.state !== 'idle') return;
    if (!this.focusSystem?.consume(1)) {
      console.log('[BattleManager] Focus not enough');
      return;
    }
    this.state = 'casting';
    director.getScene()!.getComponentInChildren('cc.Director');
    // 时停：将游戏时间缩放设为 0
    director.getScene();
    // TODO: director.setTimeScale(this.CAST_TIME_SCALE) — 在 CC3.x 中通过 game.frameRate 或 Scheduler 实现
    this.voiceEngine?.start();
  }

  /** 语音识别完成后恢复时间 */
  private endCast(): void {
    this.voiceEngine?.stop();
    // TODO: 恢复时间缩放
    this.state = 'idle';
  }

  /** 收到解析完成的咒语 */
  private onSpellCast(spell: SpellCast): void {
    console.log(`[BattleManager] Cast: ${spell.label}`);
    this.character?.castSpell(spell);
  }

  /** 识别到未知音节，给玩家提示（A2 发现机制） */
  private onUnknownSyllable(raw: string): void {
    console.log(`[BattleManager] Unknown syllable: "${raw}" — no element found`);
    // TODO: 在 UI 上显示「未知咒语」提示
  }

  getState(): BattleState {
    return this.state;
  }
}
