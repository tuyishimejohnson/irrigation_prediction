import confusion from "./assets/images/confusion.png";
import distribution from "./assets/images/moisture.png";
import moisture from "./assets/images/output.png";
import output from "./assets/images/distribution.png";

const Results = () => {
  return (
    <div>
      <div>
        <div className="flex gap-10">
          <div>
            <img src={moisture} alt="moisture" />
            <img src={distribution} alt="distribution" />
          </div>
          <div>
            <img src={confusion} alt="confusion" />
            <img src={output} alt="output" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
