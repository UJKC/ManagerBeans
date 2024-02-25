import React from 'react';

const CurrentYear = () => {
  const currentYear = new Date().getFullYear();

  return (
    <b>{currentYear}</b>
  );
};

export default CurrentYear;
