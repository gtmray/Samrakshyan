import { isRefObject } from '../../utils/is-ref-object.mjs';
import { useContext } from 'react';
import { SwitchLayoutGroupContext } from '../../context/SwitchLayoutGroupContext.mjs';

function useProjection(projectionId, { layoutId, layout, drag, dragConstraints, layoutScroll }, visualElement, ProjectionNodeConstructor) {
    var _a;
    const initialPromotionConfig = useContext(SwitchLayoutGroupContext);
    if (!ProjectionNodeConstructor ||
        !visualElement ||
        (visualElement === null || visualElement === void 0 ? void 0 : visualElement.projection)) {
        return;
    }
    visualElement.projection = new ProjectionNodeConstructor(projectionId, visualElement.getLatestValues(), (_a = visualElement.parent) === null || _a === void 0 ? void 0 : _a.projection);
    visualElement.projection.setOptions({
        layoutId,
        layout,
        alwaysMeasureLayout: Boolean(drag) || (dragConstraints && isRefObject(dragConstraints)),
        visualElement,
        scheduleRender: () => visualElement.scheduleRender(),
        /**
         * TODO: Update options in an effect. This could be tricky as it'll be too late
         * to update by the time layout animations run.
         * We also need to fix this safeToRemove by linking it up to the one returned by usePresence,
         * ensuring it gets called if there's no potential layout animations.
         *
         */
        animationType: typeof layout === "string" ? layout : "both",
        initialPromotionConfig,
        layoutScroll,
    });
}

export { useProjection };
