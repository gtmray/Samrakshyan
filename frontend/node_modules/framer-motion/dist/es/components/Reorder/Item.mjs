import { __rest } from 'tslib';
import { invariant } from 'hey-listen';
import * as React from 'react';
import { forwardRef, useContext, useRef, useEffect } from 'react';
import { ReorderContext } from '../../context/ReorderContext.mjs';
import { motion } from '../../render/dom/motion.mjs';
import { useConstant } from '../../utils/use-constant.mjs';
import { useMotionValue } from '../../value/use-motion-value.mjs';
import { useTransform } from '../../value/use-transform.mjs';
import { isMotionValue } from '../../value/utils/is-motion-value.mjs';

function useDefaultMotionValue(value, defaultValue = 0) {
    return isMotionValue(value) ? value : useMotionValue(defaultValue);
}
function ReorderItem(_a, externalRef) {
    var { children, style, value, as = "li", onDrag, layout = true } = _a, props = __rest(_a, ["children", "style", "value", "as", "onDrag", "layout"]);
    const Component = useConstant(() => motion(as));
    const context = useContext(ReorderContext);
    const point = {
        x: useDefaultMotionValue(style === null || style === void 0 ? void 0 : style.x),
        y: useDefaultMotionValue(style === null || style === void 0 ? void 0 : style.y),
    };
    const zIndex = useTransform([point.x, point.y], ([latestX, latestY]) => latestX || latestY ? 1 : "unset");
    const measuredLayout = useRef(null);
    invariant(Boolean(context), "Reorder.Item must be a child of Reorder.Group");
    const { axis, registerItem, updateOrder } = context;
    useEffect(() => {
        registerItem(value, measuredLayout.current);
    }, [context]);
    return (React.createElement(Component, Object.assign({ drag: axis }, props, { dragSnapToOrigin: true, style: Object.assign(Object.assign({}, style), { x: point.x, y: point.y, zIndex }), layout: layout, onDrag: (event, gesturePoint) => {
            const { velocity } = gesturePoint;
            velocity[axis] &&
                updateOrder(value, point[axis].get(), velocity[axis]);
            onDrag === null || onDrag === void 0 ? void 0 : onDrag(event, gesturePoint);
        }, onLayoutMeasure: (measured) => {
            measuredLayout.current = measured;
        }, ref: externalRef }), children));
}
const Item = forwardRef(ReorderItem);

export { Item, ReorderItem };
