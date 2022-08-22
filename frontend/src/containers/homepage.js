import Image from "next/image";
import React, { useState } from "react";
import ButtonDesign from "./button/buttonDesign";
import dynamic from "next/dynamic";
import { FaPause, FaPlay, FaStop, FaTimes } from "react-icons/fa";
const Waveform = dynamic(() => import("../components/wavesurfer/waveform"), { ssr: false });
export default function Homepage() {
  const [isAudio, setAudio] = useState(null);
  let fileInput;
  const [currentPosition,setPosition] = useState();
  return (
    <div className="flex lg:flex-row sm:flex-col w-full h-full lg:mt-32 sm:mt-16 lg:px-20 sm:px-4 justify-center  sm:space-y-10 lg:space-y-0 lg:space-x-32 sm:space-x-0 items-center pb-20">
      <Image src="/bird.png" height={350} width={350} />
      <div className="flex flex-col items-center space-y-3 lg:w-5/12 sm:w-full">
        <p className="lg:text-4xl sm:text-3xl font-bold">Helping you </p>
        <p className="lg:text-3xl sm:text-2xl">to get information about</p>
        <p className="lg:text-3xl sm:text-2xl"> recorded Bird sound.</p>
        <Waveform/>
        </div>
       
      </div>
    
  );
}
