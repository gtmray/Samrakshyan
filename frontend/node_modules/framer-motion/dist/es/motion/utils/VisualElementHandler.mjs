import React__default from 'react';

class VisualElementHandler extends React__default.Component {
    /**
     * Update visual element props as soon as we know this update is going to be commited.
     */
    getSnapshotBeforeUpdate() {
        this.updateProps();
        return null;
    }
    componentDidUpdate() { }
    updateProps() {
        const { visualElement, props } = this.props;
        if (visualElement)
            visualElement.setProps(props);
    }
    render() {
        return this.props.children;
    }
}

export { VisualElementHandler };
