import { checkIfControllingVariants, isVariantLabel } from '../../render/utils/variants.mjs';

function getCurrentTreeVariants(props, context) {
    if (checkIfControllingVariants(props)) {
        const { initial, animate } = props;
        return {
            initial: initial === false || isVariantLabel(initial)
                ? initial
                : undefined,
            animate: isVariantLabel(animate) ? animate : undefined,
        };
    }
    return props.inherit !== false ? context : {};
}

export { getCurrentTreeVariants };
