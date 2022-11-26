import { __rest } from 'tslib';
import { useContext } from 'react';
import { isAnimationControls } from '../../animation/utils/is-animation-controls.mjs';
import { PresenceContext } from '../../context/PresenceContext.mjs';
import { checkIfControllingVariants, checkIfVariantNode, resolveVariantFromProps } from '../../render/utils/variants.mjs';
import { useConstant } from '../../utils/use-constant.mjs';
import { resolveMotionValue } from '../../value/utils/resolve-motion-value.mjs';
import { MotionContext } from '../../context/MotionContext/index.mjs';

function makeState({ scrapeMotionValuesFromProps, createRenderState, onMount, }, props, context, presenceContext) {
    const state = {
        latestValues: makeLatestValues(props, context, presenceContext, scrapeMotionValuesFromProps),
        renderState: createRenderState(),
    };
    if (onMount) {
        state.mount = (instance) => onMount(props, instance, state);
    }
    return state;
}
const makeUseVisualState = (config) => (props, isStatic) => {
    const context = useContext(MotionContext);
    const presenceContext = useContext(PresenceContext);
    return isStatic
        ? makeState(config, props, context, presenceContext)
        : useConstant(() => makeState(config, props, context, presenceContext));
};
function makeLatestValues(props, context, presenceContext, scrapeMotionValues) {
    const values = {};
    const blockInitialAnimation = (presenceContext === null || presenceContext === void 0 ? void 0 : presenceContext.initial) === false;
    const motionValues = scrapeMotionValues(props);
    for (const key in motionValues) {
        values[key] = resolveMotionValue(motionValues[key]);
    }
    let { initial, animate } = props;
    const isControllingVariants = checkIfControllingVariants(props);
    const isVariantNode = checkIfVariantNode(props);
    if (context &&
        isVariantNode &&
        !isControllingVariants &&
        props.inherit !== false) {
        initial !== null && initial !== void 0 ? initial : (initial = context.initial);
        animate !== null && animate !== void 0 ? animate : (animate = context.animate);
    }
    const initialAnimationIsBlocked = blockInitialAnimation || initial === false;
    const variantToSet = initialAnimationIsBlocked ? animate : initial;
    if (variantToSet &&
        typeof variantToSet !== "boolean" &&
        !isAnimationControls(variantToSet)) {
        const list = Array.isArray(variantToSet) ? variantToSet : [variantToSet];
        list.forEach((definition) => {
            const resolved = resolveVariantFromProps(props, definition);
            if (!resolved)
                return;
            const { transitionEnd, transition } = resolved, target = __rest(resolved, ["transitionEnd", "transition"]);
            for (const key in target) {
                let valueTarget = target[key];
                if (Array.isArray(valueTarget)) {
                    /**
                     * Take final keyframe if the initial animation is blocked because
                     * we want to initialise at the end of that blocked animation.
                     */
                    const index = initialAnimationIsBlocked
                        ? valueTarget.length - 1
                        : 0;
                    valueTarget = valueTarget[index];
                }
                if (valueTarget !== null) {
                    values[key] = valueTarget;
                }
            }
            for (const key in transitionEnd)
                values[key] = transitionEnd[key];
        });
    }
    return values;
}

export { makeUseVisualState };
