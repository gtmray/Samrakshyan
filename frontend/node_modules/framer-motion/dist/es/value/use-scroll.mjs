import { __rest } from 'tslib';
import { scroll } from '@motionone/dom';
import { motionValue } from './index.mjs';
import { useConstant } from '../utils/use-constant.mjs';
import { useIsomorphicLayoutEffect } from '../utils/use-isomorphic-effect.mjs';

const createScrollMotionValues = () => ({
    scrollX: motionValue(0),
    scrollY: motionValue(0),
    scrollXProgress: motionValue(0),
    scrollYProgress: motionValue(0),
});
function useScroll(_a = {}) {
    var { container, target } = _a, options = __rest(_a, ["container", "target"]);
    const values = useConstant(createScrollMotionValues);
    useIsomorphicLayoutEffect(() => {
        return scroll(({ x, y }) => {
            values.scrollX.set(x.current);
            values.scrollXProgress.set(x.progress);
            values.scrollY.set(y.current);
            values.scrollYProgress.set(y.progress);
        }, Object.assign(Object.assign({}, options), { container: (container === null || container === void 0 ? void 0 : container.current) || undefined, target: (target === null || target === void 0 ? void 0 : target.current) || undefined }));
    }, []);
    return values;
}

export { useScroll };
