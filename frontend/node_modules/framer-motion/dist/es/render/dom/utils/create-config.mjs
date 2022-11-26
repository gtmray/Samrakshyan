import { isSVGComponent } from './is-svg-component.mjs';
import { createUseRender } from '../use-render.mjs';
import { svgMotionConfig } from '../../svg/config-motion.mjs';
import { htmlMotionConfig } from '../../html/config-motion.mjs';

function createDomMotionConfig(Component, { forwardMotionProps = false }, preloadedFeatures, createVisualElement, projectionNodeConstructor) {
    const baseConfig = isSVGComponent(Component)
        ? svgMotionConfig
        : htmlMotionConfig;
    return Object.assign(Object.assign({}, baseConfig), { preloadedFeatures, useRender: createUseRender(forwardMotionProps), createVisualElement,
        projectionNodeConstructor,
        Component });
}

export { createDomMotionConfig };
