import React from 'react'

export default function buttonDesign({text,onClickHandler,icon,className}) {
  return (
    <button type='button' onClick={onClickHandler} className={`flex rounded-xl  ${className}  space-x-4 items-center text-lg px-4 py-3`}>
      {icon}
    <p>{text}</p>
    </button>
  )
}
