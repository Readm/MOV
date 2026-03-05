import { _decorator, Component, Vec2, input, Input, KeyCode } from 'cc';
import { SpellCast } from '../spell/SpellSystem';

const { ccclass, property } = _decorator;

/**
 * 玩家角色
 * 负责：移动、HP/SP 管理、接收并执行咒语
 */
@ccclass('Character')
export class Character extends Component {
  @property maxHp = 100;
  @property maxSp = 100;
  @property moveSpeed = 150;

  private hp = 100;
  private sp = 100;
  private moveDir = new Vec2(0, 0);

  onLoad(): void {
    input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    input.on(Input.EventType.KEY_UP, this.onKeyUp, this);
  }

  onDestroy(): void {
    input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    input.off(Input.EventType.KEY_UP, this.onKeyUp, this);
  }

  update(dt: number): void {
    if (!this.moveDir.equals(Vec2.ZERO)) {
      const pos = this.node.position;
      this.node.setPosition(
        pos.x + this.moveDir.x * this.moveSpeed * dt,
        pos.y + this.moveDir.y * this.moveSpeed * dt,
        pos.z,
      );
    }
  }

  /** 接收咒语，派发对应效果 */
  castSpell(spell: SpellCast): void {
    console.log(`[Character] Casting: ${spell.label} (level ${spell.level})`);
    // TODO: 根据 spell.element / form / modifier 实例化对应的技能预制体
  }

  takeDamage(amount: number): void {
    this.hp = Math.max(0, this.hp - amount);
    if (this.hp <= 0) {
      console.log('[Character] Dead');
      // TODO: 触发死亡事件
    }
  }

  get currentHp() { return this.hp; }
  get currentSp() { return this.sp; }

  private onKeyDown(event: any): void {
    switch (event.keyCode) {
      case KeyCode.KEY_W: this.moveDir.y = 1; break;
      case KeyCode.KEY_S: this.moveDir.y = -1; break;
      case KeyCode.KEY_A: this.moveDir.x = -1; break;
      case KeyCode.KEY_D: this.moveDir.x = 1; break;
    }
  }

  private onKeyUp(event: any): void {
    switch (event.keyCode) {
      case KeyCode.KEY_W:
      case KeyCode.KEY_S: this.moveDir.y = 0; break;
      case KeyCode.KEY_A:
      case KeyCode.KEY_D: this.moveDir.x = 0; break;
    }
  }
}
