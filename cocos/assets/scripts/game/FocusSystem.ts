import { _decorator, Component } from 'cc';

const { ccclass, property } = _decorator;

/**
 * 专注值（Focus）系统
 * Focus 是时停施法的独立资源，随时间自然恢复
 */
@ccclass('FocusSystem')
export class FocusSystem extends Component {
  @property max = 5;
  @property regenPerSecond = 1;

  private current = 5;

  get value() { return this.current; }
  get isFull() { return this.current >= this.max; }
  get isEmpty() { return this.current <= 0; }

  /** 消耗 Focus，返回是否成功 */
  consume(amount = 1): boolean {
    if (this.current < amount) return false;
    this.current -= amount;
    return true;
  }

  update(dt: number): void {
    if (this.current < this.max) {
      this.current = Math.min(this.max, this.current + this.regenPerSecond * dt);
    }
  }
}
