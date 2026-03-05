import { _decorator, Component, Node, input, Input, KeyCode } from 'cc';
import { BattleManager } from '../game/BattleManager';

const { ccclass, property } = _decorator;

/**
 * 战斗场景根组件
 * 负责：场景初始化、玩家输入路由（施法键）
 */
@ccclass('BattleScene')
export class BattleScene extends Component {
  @property(Node) battleManagerNode: Node | null = null;

  private battleManager: BattleManager | null = null;

  onLoad(): void {
    this.battleManager = this.battleManagerNode?.getComponent(BattleManager) ?? null;
    input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
  }

  onDestroy(): void {
    input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
  }

  private onKeyDown(event: any): void {
    // 空格键 = 触发施法（时停 + 开始语音识别）
    if (event.keyCode === KeyCode.SPACE) {
      this.battleManager?.startCast();
    }
  }
}
