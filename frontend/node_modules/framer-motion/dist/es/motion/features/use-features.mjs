import * as React from 'react';
import { useContext } from 'react';
import { env } from '../../utils/process.mjs';
import { featureDefinitions } from './definitions.mjs';
import { invariant } from 'hey-listen';
import { LazyContext } from '../../context/LazyContext.mjs';

const featureNames = Object.keys(featureDefinitions);
const numFeatures = featureNames.length;
/**
 * Load features via renderless components based on the provided MotionProps.
 */
function useFeatures(props, visualElement, preloadedFeatures) {
    const features = [];
    const lazyContext = useContext(LazyContext);
    if (!visualElement)
        return null;
    /**
     * If we're in development mode, check to make sure we're not rendering a motion component
     * as a child of LazyMotion, as this will break the file-size benefits of using it.
     */
    if (env !== "production" && preloadedFeatures && lazyContext.strict) {
        invariant(false, "You have rendered a `motion` component within a `LazyMotion` component. This will break tree shaking. Import and render a `m` component instead.");
    }
    for (let i = 0; i < numFeatures; i++) {
        const name = featureNames[i];
        const { isEnabled, Component } = featureDefinitions[name];
        /**
         * It might be possible in the future to use this moment to
         * dynamically request functionality. In initial tests this
         * was producing a lot of duplication amongst bundles.
         */
        if (isEnabled(props) && Component) {
            features.push(React.createElement(Component, Object.assign({ key: name }, props, { visualElement: visualElement })));
        }
    }
    return features;
}

export { useFeatures };
