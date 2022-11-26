import * as React from 'react';
import { useContext, useRef, useMemo } from 'react';
import { LayoutGroupContext } from '../../context/LayoutGroupContext.mjs';
import { DeprecatedLayoutGroupContext } from '../../context/DeprecatedLayoutGroupContext.mjs';
import { useForceUpdate } from '../../utils/use-force-update.mjs';
import { nodeGroup } from '../../projection/node/group.mjs';

const shouldInheritGroup = (inherit) => inherit === true;
const shouldInheritId = (inherit) => shouldInheritGroup(inherit === true) || inherit === "id";
const LayoutGroup = ({ children, id, inheritId, inherit = true, }) => {
    var _a, _b;
    // Maintain backwards-compatibility with inheritId until 7.0
    if (inheritId !== undefined)
        inherit = inheritId;
    const layoutGroupContext = useContext(LayoutGroupContext);
    const deprecatedLayoutGroupContext = useContext(DeprecatedLayoutGroupContext);
    const [forceRender, key] = useForceUpdate();
    const context = useRef(null);
    const upstreamId = (_a = layoutGroupContext.id) !== null && _a !== void 0 ? _a : deprecatedLayoutGroupContext;
    if (context.current === null) {
        if (shouldInheritId(inherit) && upstreamId) {
            id = id ? upstreamId + "-" + id : upstreamId;
        }
        context.current = {
            id,
            group: shouldInheritGroup(inherit)
                ? (_b = layoutGroupContext === null || layoutGroupContext === void 0 ? void 0 : layoutGroupContext.group) !== null && _b !== void 0 ? _b : nodeGroup()
                : nodeGroup(),
        };
    }
    const memoizedContext = useMemo(() => (Object.assign(Object.assign({}, context.current), { forceRender })), [key]);
    return (React.createElement(LayoutGroupContext.Provider, { value: memoizedContext }, children));
};

export { LayoutGroup };
