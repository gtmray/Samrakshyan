import Image from 'next/image'
import React from 'react'

export default function Navbar() {
  return (
    <nav className="bg-white w-full sticky top-0 shadow-md content-center text-black z-10 py-3 ">
    <div className=' flex flex-row w-full items-center pl-10 space-x-5'>
     <Image src="/favicon.ico" height={50} width={50}></Image> 
    <p className=' text-xl font-bold'>संरक्षण : An Endangered Birds Recognition Portal </p>
    </div>
   </nav>
  )
}
