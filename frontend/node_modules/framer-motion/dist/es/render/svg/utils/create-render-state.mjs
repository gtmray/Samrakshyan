import { createHtmlRenderState } from '../../html/utils/create-render-state.mjs';

const createSvgRenderState = () => (Object.assign(Object.assign({}, createHtmlRenderState()), { attrs: {} }));

export { createSvgRenderState };
