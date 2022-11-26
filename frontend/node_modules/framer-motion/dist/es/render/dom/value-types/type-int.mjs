import { number } from 'style-value-types';

const int = Object.assign(Object.assign({}, number), { transform: Math.round });

export { int };
