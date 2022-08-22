import { AnimationType } from '../render/utils/types.mjs';
import { useDomEvent } from '../events/use-dom-event.mjs';

/**
 *
 * @param props
 * @param ref
 * @internal
 */
function useFocusGesture({ whileFocus, visualElement }) {
    const onFocus = () => {
        var _a;
        (_a = visualElement.animationState) === null || _a === void 0 ? void 0 : _a.setActive(AnimationType.Focus, true);
    };
    const onBlur = () => {
        var _a;
        (_a = visualElement.animationState) === null || _a === void 0 ? void 0 : _a.setActive(AnimationType.Focus, false);
    };
    useDomEvent(visualElement, "focus", whileFocus ? onFocus : undefined);
    useDomEvent(visualElement, "blur", whileFocus ? onBlur : undefined);
}

export { useFocusGesture };
