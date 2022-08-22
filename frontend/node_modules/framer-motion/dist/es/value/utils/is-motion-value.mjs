const isMotionValue = (value) => {
    return Boolean(value !== null && typeof value === "object" && value.getVelocity);
};

export { isMotionValue };
