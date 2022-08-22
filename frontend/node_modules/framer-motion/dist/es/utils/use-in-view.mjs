import { useState, useEffect } from 'react';
import { inView } from '@motionone/dom';

function useInView(ref, { root, margin, amount, once = false } = {}) {
    const [isInView, setInView] = useState(false);
    useEffect(() => {
        var _a;
        if (!ref.current || (once && isInView))
            return;
        const onEnter = () => {
            setInView(true);
            return once ? undefined : () => setInView(false);
        };
        const options = {
            root: (_a = root === null || root === void 0 ? void 0 : root.current) !== null && _a !== void 0 ? _a : undefined,
            margin,
            amount: amount === "some" ? "any" : amount,
        };
        return inView(ref.current, onEnter, options);
    }, [root, ref, margin, once]);
    return isInView;
}

export { useInView };
