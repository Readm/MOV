import { _decorator, Component, director } from 'cc';

const { ccclass } = _decorator;

/**
 * 主菜单场景
 */
@ccclass('MenuScene')
export class MenuScene extends Component {
  startGame(): void {
    director.loadScene('Battle');
  }
}
