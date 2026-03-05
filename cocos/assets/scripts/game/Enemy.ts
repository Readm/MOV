import { _decorator, Component, Vec2 } from 'cc';
import { Element, Form } from '../spell/SpellDatabase';

const { ccclass, property } = _decorator;

export type EnemyState = 'idle' | 'chase' | 'windup' | 'attack' | 'stunned' | 'dead';

export interface StatusEffect {
  type: 'burn' | 'freeze' | 'paralyze' | 'knockback';
  duration: number;
}

/**
 * 敌人基类
 * 三层设计：形态弱点 / 状态效果 / 行为前摇
 */
@ccclass('Enemy')
export class Enemy extends Component {
  @property maxHp = 50;
  @property moveSpeed = 60;
  /** 形态弱点：受到此形态攻击时伤害翻倍 */
  @property formWeakness: string = 'bolt';
  /** 行为前摇时长（秒），前摇中可被打断 */
  @property windupDuration = 1.2;

  protected hp = 50;
  protected state: EnemyState = 'idle';
  protected statusEffects: StatusEffect[] = [];
  private windupTimer = 0;

  update(dt: number): void {
    this.updateStatus(dt);
    this.updateBehavior(dt);
  }

  /**
   * 承受伤害
   * @param amount 基础伤害
   * @param sourceForm 攻击形态（用于判断弱点加成）
   * @param sourceElement 攻击元素（用于附加状态）
   */
  takeDamage(amount: number, sourceForm: Form | null, sourceElement: Element): void {
    let finalAmount = amount;

    // 形态弱点：翻倍
    if (sourceForm && sourceForm === this.formWeakness) {
      finalAmount *= 2;
      console.log(`[Enemy] Weakness hit! ${sourceForm} x2`);
    }

    this.hp -= finalAmount;

    // 元素状态效果
    this.applyElementStatus(sourceElement);

    if (this.hp <= 0) {
      this.onDeath();
    }
  }

  /** 打断前摇（玩家在前摇期间施放对应技能可打断） */
  interrupt(): void {
    if (this.state === 'windup') {
      console.log('[Enemy] Interrupted!');
      this.state = 'idle';
      this.windupTimer = 0;
    }
  }

  private applyElementStatus(element: Element): void {
    const effectMap: Record<Element, StatusEffect> = {
      fire:    { type: 'burn',      duration: 3 },
      ice:     { type: 'freeze',    duration: 2 },
      thunder: { type: 'paralyze',  duration: 1.5 },
      earth:   { type: 'knockback', duration: 0.5 },
    };
    this.statusEffects.push(effectMap[element]);
  }

  private updateStatus(dt: number): void {
    this.statusEffects = this.statusEffects
      .map(e => ({ ...e, duration: e.duration - dt }))
      .filter(e => e.duration > 0);
  }

  private updateBehavior(dt: number): void {
    if (this.statusEffects.some(e => e.type === 'freeze' || e.type === 'paralyze')) return;

    switch (this.state) {
      case 'windup':
        this.windupTimer -= dt;
        if (this.windupTimer <= 0) {
          this.state = 'attack';
          this.performAttack();
        }
        break;
      // TODO: chase / idle 行为在子类中实现
    }
  }

  protected startWindup(): void {
    this.state = 'windup';
    this.windupTimer = this.windupDuration;
    // TODO: 播放前摇动画，通知 UI 显示警示
  }

  protected performAttack(): void {
    // 子类重写
    this.state = 'idle';
  }

  protected onDeath(): void {
    this.state = 'dead';
    // TODO: 播放死亡动画，发出掉落事件
    this.node.destroy();
  }
}
