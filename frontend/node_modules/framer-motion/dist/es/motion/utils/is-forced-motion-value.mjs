import { scaleCorrectors } from '../../projection/styles/scale-correction.mjs';
import { isTransformProp, isTransformOriginProp } from '../../render/html/utils/transform.mjs';

function isForcedMotionValue(key, { layout, layoutId }) {
    return (isTransformProp(key) ||
        isTransformOriginProp(key) ||
        ((layout || layoutId !== undefined) &&
            (!!scaleCorrectors[key] || key === "opacity")));
}

export { isForcedMotionValue };
