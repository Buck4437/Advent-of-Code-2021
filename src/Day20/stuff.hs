let [strCode, input] = raw.split("\n\n");

const DECODER = strCode.split("").map(x => x === "#");

class Grid {
  constructor (string) {
    const arr = string.split(/\n/g).map(x => x.split(""));
    this.steps = 0;
    this.data = [];
    this.future = [];
    this.newTile = false;
    this.rows = arr.length;
    this.cols = arr[0].length;
    for (let x = 0; x < arr.length; x++) {
      this.data.push([]);
      this.future.push([]);
      for (let y = 0; y < arr[0].length; y++) {
        this.data[x][y] = (arr[x][y] === "#");
      }
    }
  }

  checkNewTile() {
    this.newTile = DECODER[this.newTile ? 511 : 0];
  }

  litCode(x0, y0) {
    let lit = 0;
    for (let x = x0 - 1; x <= x0 + 1; x++) {
      for (let y = y0 - 1; y <= y0 + 1; y++) {
        lit *= 2;
        if (this.isLit(x, y)) lit++;
      }
    }
    return lit;
  }

  isLit(x, y) {
    if (!this.validTile(x, y)) return this.newTile;
    return this.data[x][y];
  }

  validTile(x, y) {
    return (x >= 0 && y >= 0 && x < this.rows && y < this.cols)
  }

  stepTile(x, y) {
    let code = this.litCode(x, y);
    return DECODER[code]; // A value between 0 and 511.
  }

  step(times) {
    for (let i = 0; i < times; i++) {
      // Insert new tiles around the borders
      this.data.unshift([]);
      this.future.unshift([]);
      this.data.push([]);
      this.future.push([]);
      this.rows += 2;
      for (let y = 0; y < this.cols; y++) {
        this.data[0].push(this.newTile);
        this.data[this.data.length - 1].push(this.newTile);
      }
      for (let x = 0; x < this.rows; x++) {
        this.data[x].push(this.newTile);
        this.data[x].unshift(this.newTile);
      }
      this.cols += 2;

      for (let x = 0; x < this.rows; x++) {
        for (let y = 0; y < this.cols; y++) {
          this.future[x][y] = this.stepTile(x, y);
        }
      }
      this.checkNewTile()
      this.steps++;
      this.data = this.future.map(row => row.slice()); // Thanks Isatis.
    }

    let lit = 0;
    for (let x = 0; x < this.rows; x++) {
      for (let y = 0; y < this.cols; y++) {
        if (this.data[x][y]) lit++;
      }
    }
    return lit;
  }

  toString() {
    let output = ""
    for (let x = 0; x < this.rows; x++) {
      output += "\n";
      for (let y = 0; y < this.cols; y++) {
        if (this.data[x][y]) output += "#";
        else output += "."
      }
    }
    return output;
  }
}

input = new Grid(input);

console.log(input.step(2))
console.log(input.step(48)) // 50 - 2

// console.log(input.toString())