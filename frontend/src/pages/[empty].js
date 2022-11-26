import React, { useEffect } from 'react';

export default function Reload() {
  useEffect(() => {
    window.location.replace('/');
  }, []);
  return <div />;
}