// ─────────────────────────────────────────────────────────────
// MOV 像素风精灵系统
// 所有精灵为 16×16 像素，统一暗黑魔幻风格
// ─────────────────────────────────────────────────────────────

const PAL = {
  '.': null,
  // ── 通用轮廓 ──
  'K': '#080810',
  // ── 玩家（青色法师）──
  'T': '#1cb8ad',  // 青绿长袍
  't': '#5deee6',  // 高光
  'D': '#0b5e58',  // 暗面/褶皱
  'F': '#f5d5a8',  // 皮肤
  'f': '#c9956a',  // 皮肤暗
  'i': '#e8c040',  // 金色（权杖）
  // ── 哥布林（暗红）──
  'R': '#cc3030',  // 皮肤红
  'r': '#7a1010',  // 暗红
  'G': '#40cc40',  // 绿眼
  'Y': '#eeee44',  // 牙齿黄
  // ── 史莱姆（毒绿）──
  'L': '#70e870',  // 亮绿
  'l': '#38b838',  // 中绿
  'M': '#186018',  // 暗绿
  'W': '#c0ffc0',  // 高光白绿
  // ── 石像鬼（石灰棕）──
  'O': '#aa8855',  // 石面
  'o': '#6a5030',  // 石暗
  'Q': '#3a2810',  // 裂缝
  'C': '#d0aa70',  // 高光石
  'E': '#ee2222',  // 红眼
  // ── 地板 ──
  '1': '#13131f',  // 石板暗
  '2': '#1b1b2e',  // 石板中
  '3': '#23233e',  // 石板亮
  '4': '#0d0d16',  // 缝隙
  '5': '#202038',  // 微亮点
};

// ── 精灵像素数据（每行恰好16字符）──
const SPRITE_DATA = {

  // 玩家：青色魔法师，俯视3/4角
  player: [
    '................',
    '......KKK.......',
    '.....KTTtK......',
    '....KTTTtTK.....',
    '...KTFfFftTK....',
    '...KTFKFftTK....',
    '...KTFfFftTK....',
    '...KTTTtTTTK....',
    '..KTTTDtDTTTK...',
    '.KTTTTDtDTTTTK..',
    'KTTTTDDtDDTTTTK.',
    '.KTTTiTtTiTTTK..',
    '..KTTTTtTTTTK...',
    '...KTTtD.DTTK...',
    '....KKK...KKK...',
    '................',
  ],

  // 玩家帧2（轻微变化，形成步行感）
  player2: [
    '................',
    '......KKK.......',
    '.....KTTtK......',
    '....KTTTtTK.....',
    '...KTFfFftTK....',
    '...KTFKFftTK....',
    '...KTFfFftTK....',
    '...KTTTtTTTK....',
    '..KTTTDtDTTTK...',
    '.KTTTTDtDTTTTK..',
    'KTTTTDDtDDTTTTK.',
    '.KTTTiTtTiTTTK..',
    '..KTTTTtTTTTK...',
    '....KTTt.TTK....',
    '.....KK.KK......',
    '................',
  ],

  // 哥布林：小型暗红肉食者
  goblin: [
    '................',
    '....KKKKKK......',
    '...KRRRRrRK.....',
    '..KRGRrRGRrK....',
    '..KRRRrRRRK.....',
    '.KRRKRrRKRRK....',
    '.KRRRKrKKRRK....',
    '.KRRRRrRRRRK....',
    'KRRRRRrRRRRRK...',
    'KRrRRRrRRRrRRK..',
    '.KRRRrRRRRRK....',
    '.KRrRRRRRrRK....',
    '.KRRKr.rKRRK....',
    '..KRRr.rRRK.....',
    '...KKr..rKK.....',
    '....KK..KK......',
  ],

  // 哥布林帧2
  goblin2: [
    '................',
    '....KKKKKK......',
    '...KRRRRrRK.....',
    '..KRGRrRGRrK....',
    '..KRRRrRRRK.....',
    '.KRRKRrRKRRK....',
    '.KRRRKrKKRRK....',
    '.KRRRRrRRRRK....',
    'KRRRRRrRRRRRK...',
    'KRrRRRrRRRrRRK..',
    '.KRRRrRRRRRK....',
    '.KRrRRRRRrRK....',
    '..KRRr.rRRK.....',
    '...KRRr.rRK.....',
    '....KKr.rKK.....',
    '.....KK.KK......',
  ],

  // 史莱姆：圆润毒绿团
  slime: [
    '................',
    '.......KK.......',
    '.....KLWLlK.....',
    '....KLLWLllK....',
    '...KLLLWLlllK...',
    '..KLLLLWLllllK..',
    '.KLLKLLWLllKLlK.',
    '.KLLLLLWLlllLlK.',
    '.KLLLLLlllllLK..',
    '.KLLLLllllllLK..',
    '..KLMMLllllMMK..',
    '..KLLLlllllLLK..',
    '...KKLLlllLKK...',
    '....KKKLLKKK....',
    '.....KKKKKK.....',
    '................',
  ],

  // 史莱姆帧2（略扁，跳动感）
  slime2: [
    '................',
    '................',
    '......KKK.......',
    '....KLLWLlK.....',
    '...KLLLWLllK....',
    '..KLLLLWLlllK...',
    '.KLLKLLWLllKLlK.',
    '.KLLLLLWLlllLlK.',
    'KLLLLLLlllllLLLK',
    '.KLLLLllllllLLK.',
    '..KLMMLllllMMK..',
    '...KLLLlllLLK...',
    '....KKLLlLKK....',
    '.....KKKKKK.....',
    '................',
    '................',
  ],

  // 石像鬼：重甲石块，大块头
  golem: [
    '................',
    '..KKKKKKKKKK....',
    '.KCCOOOOOOoK....',
    '.KCOQQQOooOK....',
    'KCOOQQOOoQooK...',
    'KCOQKEoKQOooK...',
    'KCOQKEoKQOooK...',
    'KCOOQQOOoQooK...',
    'KCOOQOOOooOoK...',
    '.KCOOOOOoooK....',
    'KCOQQOooQQOoK...',
    'KCOOOoooOOOoK...',
    '.KCOQoooQOCK....',
    '.KCOOOooOQCK....',
    '..KKKKKKKKK.....',
    '................',
  ],

  // ── 地板瓷砖（16×16，可无缝平铺）──
  floor: [
    '1221122112211221',
    '2222222222222222',
    '2333222222223332',
    '2222222222222222',
    '1222252222522221',
    '2222222222222222',
    '2222223322322222',
    '2222222222222222',
    '2222222222222222',
    '2223322222223322',
    '2222222222222222',
    '1222252222522221',
    '2222222222222222',
    '2333222222223332',
    '2222222222222222',
    '1221122112211221',
  ],

  // 墙体瓷砖
  wall: [
    '4444444444444444',
    '4OOOOOOOO2OOOO44',
    '4OoOOOOO2OoOOO44',
    '4OOOQOOo2OOOoO44',
    '4444444444444444',
    '4OOOOOO2OoOOOO44',
    '4OoOOO2OOOoOOO44',
    '4OOOQ2OoOOOOQO44',
    '4444444444444444',
    '4OOOOO2OoOOOOO44',
    '4OoOOO2OOoOOOO44',
    '4OOOOQ2OoOOOoO44',
    '4444444444444444',
    '4OOOOO2OoOOOOO44',
    '4OoOOO2OOOOOOQ44',
    '4444444444444444',
  ],
};

// ─────────────────────────────────────────────
// 精灵渲染器
// ─────────────────────────────────────────────
class SpriteRenderer {
  constructor(scale = 2) {
    this.scale = scale;
    this.cache = {};
    for (const [name, rows] of Object.entries(SPRITE_DATA)) {
      this.cache[name] = this._bake(rows, scale);
    }
    // 预烘焙受击白化版本
    for (const name of ['player','goblin','slime','golem']) {
      this.cache[name + '_hit'] = this._bakeWhite(SPRITE_DATA[name], scale);
    }
  }

  _bake(rows, scale) {
    const w = rows[0].length * scale;
    const h = rows.length * scale;
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const ctx = c.getContext('2d');
    ctx.imageSmoothingEnabled = false;
    for (let y = 0; y < rows.length; y++) {
      for (let x = 0; x < rows[y].length; x++) {
        const color = PAL[rows[y][x]];
        if (!color) continue;
        ctx.fillStyle = color;
        ctx.fillRect(x * scale, y * scale, scale, scale);
      }
    }
    return c;
  }

  _bakeWhite(rows, scale) {
    const c = this._bake(rows, scale);
    const ctx = c.getContext('2d');
    ctx.globalCompositeOperation = 'source-atop';
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, c.width, c.height);
    return c;
  }

  // 居中绘制精灵
  draw(ctx, name, x, y, opts = {}) {
    const img = this.cache[name];
    if (!img) return;
    const dx = Math.floor(x - img.width / 2);
    const dy = Math.floor(y - img.height / 2);
    ctx.save();
    if (opts.alpha !== undefined) ctx.globalAlpha = opts.alpha;
    if (opts.flipX) {
      ctx.translate(x * 2, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(img, dx + (opts.flipX ? -img.width : 0), dy);
    ctx.restore();
  }
}

// ─────────────────────────────────────────────
// 背景预渲染
// ─────────────────────────────────────────────
function createBackground(renderer, W, H) {
  const c = document.createElement('canvas');
  c.width = W; c.height = H;
  const ctx = c.getContext('2d');
  ctx.imageSmoothingEnabled = false;

  const floor = renderer.cache.floor;
  const wall  = renderer.cache.wall;
  const tw = floor.width;  // tile width  = 32 (16px * scale 2)
  const th = floor.height; // tile height = 32

  const UI_H = 40; // UI 顶栏高度

  // 地板区域
  for (let y = UI_H; y < H; y += th) {
    for (let x = 0; x < W; x += tw) {
      ctx.drawImage(floor, x, y);
    }
  }

  // 上边墙
  for (let x = 0; x < W; x += tw) {
    ctx.drawImage(wall, x, UI_H);
  }
  // 下边墙
  for (let x = 0; x < W; x += tw) {
    ctx.drawImage(wall, x, H - th);
  }
  // 左边墙
  for (let y = UI_H; y < H; y += th) {
    ctx.drawImage(wall, 0, y);
  }
  // 右边墙
  for (let y = UI_H; y < H; y += th) {
    ctx.drawImage(wall, W - tw, y);
  }

  // 角落加深
  ctx.fillStyle = 'rgba(0,0,0,0.35)';
  [[0,UI_H],[W-tw,UI_H],[0,H-th],[W-tw,H-th]].forEach(([x,y]) => {
    ctx.fillRect(x, y, tw, th);
  });

  return c;
}
