import ButtonDesign from "../../containers/button/buttonDesign";
import { FaPause, FaPlay, FaStop, FaTimes } from "react-icons/fa";
import Wavesurfer from "wavesurfer.js";
import { useEffect, useRef,useState } from "react";
import { CircularProgress } from "@mui/material";
// import { Flex, Button } from "@chakar-ui/react";

const Waveform = () => {
  const waveform = useRef(null);
  const [isAudio, setAudio] = useState(false);
  const [value,setValue] = useState();
  const [isLoading,setLoading] = useState(false);
  const [currentPosition, setPosition] = useState();
  let fileInput;
    const handlePlay = () => {
      if(waveform.current.isPlaying())
      {
        waveform.current.pause();
        setPosition("Pause");
      }else{
        waveform.current.play();
        setPosition("Play");
      }
       
      };
      // const handlePause = () => {
       
      //   setPosition("Pause");
      // };
      const handleStop = () => {
        waveform.current.stop();
        setPosition("Stop");
      };
        
       
  const createWaveform = (e) => {
    setAudio(true);
    var file = e.target.files[0];
    if (file) {
        waveform.current.load(URL.createObjectURL(file));
        waveform.current.play();
        setPosition("Play");
    }
  };

  useEffect(() => {
    // Check if wavesurfer object is already created.
    if (!waveform.current) {
      // Create a wavesurfer object
      waveform.current = Wavesurfer.create({
              barWidth: 3,
              barRadius: 3,
              barGap: 2,
              barMinHeight: 1,
              barHeight:20,
              cursorWidth: 1,
              container: "#waveform",
              backend: "MediaElement",
              height: 200,
              progressColor: "#4353FF",
              responsive: true,
              waveColor: "#567FFF",
              cursorColor: "#567FFF",
      });
      // waveform.current.load("/spinybabbler.mp3");
    }
  }, []);
    return (
    <div className="w-full">
      <div className="flex justify-center">
      <input
        type="file"
        accept="audio/*"
        className="opacity-0 w-0 h-2"
        ref={(fileinput) => (fileInput = fileinput)}
        onChange={createWaveform}
      />
      {
        !isAudio &&  <ButtonDesign
        text="Import Sound"
        onClickHandler={() => fileInput.click()}
        className="bg-buttonColor w-[145px] text-white"
      />
      
      }</div>
      <div className="lg:w-[600px] sm:w-full  space-y-5  ">
       {isAudio && <div className="flex flex-col items-end">
          <button
            onClick={() => {
              setAudio(false);
              setPosition("");
              setValue(null);
              waveform.current.stop();
            }}
            className="py-3 px-3"
          >
            <FaTimes className="h-8 w-4 text-lightBlackColor"></FaTimes>
          </button>
            {/* <div id="waveform"></div> */}
          {/* <img src="/signal.png" className="h-[300px] w-[600px]" /> */}
        </div>}
         <div id="waveform" className={isAudio?"visible":"hidden"}></div>
       {isAudio && 
       <div className="space-y-5">
       <div className="flex justify-between px-5">
          <ButtonDesign
            text={ currentPosition == "Play"?"Pause":"Play"}
            onClickHandler={handlePlay}
            className={` ${
              currentPosition == "Play" ||  currentPosition == "Pause"
                ? "bg-buttonColor text-white"
                : "bg-gray-400 text-black"
            } hover:bg-buttonColor group hover:text-white`}
            icon={
              currentPosition == "Play"?
              <FaPause
                className={`h-4 w-4 ${
                  currentPosition == "Play" ? "text-white" : "text-black"
                } group-hover:text-white `}
              />:<FaPlay
              className={`h-4 w-4 ${
                currentPosition == "Pause" ? "text-white" : "text-black"
              }  group-hover:text-white`}
            />
            }
          />
          {/* <ButtonDesign
            text="Pause"
            onClickHandler={handlePause}
            className={`${
              currentPosition == "Pause"
                ? "bg-buttonColor text-white"
                : "bg-gray-400 text-black"
            } hover:bg-buttonColor group hover:text-white`}
            icon={
              <FaPause
                className={`h-4 w-4 ${
                  currentPosition == "Pause" ? "text-white" : "text-black"
                }  group-hover:text-white`}
              />
            }
          /> */}
          <ButtonDesign
            text="Stop"
            onClickHandler={handleStop}
            className={`${
              currentPosition == "Stop"
                ? "bg-buttonColor text-white"
                : "bg-gray-400 text-black"
            } hover:bg-buttonColor group hover:text-white`}
            icon={
              <FaStop
                className={`h-4 w-4 ${
                  currentPosition == "Stop" ? "text-white" : "text-black"
                } group-hover:text-white`}
              />
            }
          />
        </div>
        <div className="flex  justify-center">
            <ButtonDesign text="Predict the sound"
            className="bg-gray-400"

            onClickHandler={()=>{
              setLoading(true);
              setTimeout(()=>{
                setValue("Spiny Babbler");
                setLoading(false);
              },2000)
            }}/>
           
        </div>
        {value? <p className=" pt-2 text-center">80% match with {value} </p>:isLoading && <div className="flex pt-2 justify-center"><CircularProgress size={40}/></div>}
        </div>}
      </div>
    </div>
  // ) : (
  //   <div className="w-[300px] h-[100px] justify-center items-center flex">
  //     <CircularProgress size={40} />
  //   </div>
  );
};

export default Waveform;
