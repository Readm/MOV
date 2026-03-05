import { _decorator, Component, Label, Node, tween, Vec3 } from 'cc';
import { SpellCast } from '../spell/SpellSystem';

const { ccclass, property } = _decorator;

/**
 * 咒语反馈 UI
 * 显示识别到的咒语名称，以及「发现」提示（A2 机制）
 */
@ccclass('SpellFeedbackUI')
export class SpellFeedbackUI extends Component {
  @property(Label) spellLabel: Label | null = null;
  @property(Label) discoveryLabel: Label | null = null;
  @property(Node) focusBar: Node | null = null;

  /** 显示咒语施放提示 */
  showSpellCast(spell: SpellCast): void {
    if (!this.spellLabel) return;
    this.spellLabel.string = spell.label;
    this.spellLabel.node.setScale(new Vec3(1.5, 1.5, 1));
    tween(this.spellLabel.node)
      .to(0.1, { scale: new Vec3(1, 1, 1) })
      .delay(1.5)
      .to(0.3, { scale: new Vec3(0, 0, 1) })
      .start();
  }

  /** 显示「发现新音节」提示（A2 机制） */
  showDiscovery(message: string): void {
    if (!this.discoveryLabel) return;
    this.discoveryLabel.string = message;
    this.discoveryLabel.node.active = true;
    tween(this.discoveryLabel.node)
      .delay(2)
      .call(() => { this.discoveryLabel!.node.active = false; })
      .start();
  }

  /** 更新专注值条 */
  updateFocusBar(current: number, max: number): void {
    if (!this.focusBar) return;
    const ratio = current / max;
    this.focusBar.setScale(new Vec3(ratio, 1, 1));
  }
}
