import * as math from 'mathjs';

const A = [
    [math.complex(1, 2), math.complex(0, -1)],
    [math.complex(0, -1), math.complex(2, 0)]
];
const b = [math.complex(1, 0), math.complex(0, 0)];

const x = math.lusolve(A, b);
console.log(x);
console.log(x[0][0].toString(), x[1][0].toString());
