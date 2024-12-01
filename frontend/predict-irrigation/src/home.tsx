import irrigation from "./assets/images/erwan-hesry-1q75BReKpms-unsplash.jpg";
import Button from "./components/button";
import Footer from "./components/footer";
import { NavLink } from "react-router-dom";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import graph2 from "./assets/images/rwanda-gdp-from-agriculture.png";

interface Structure {
  percentage: number;
  description: string;
}

const structureDetails: Structure[] = [
  {
    percentage: 66,
    description: "Total population are engaged in Agriculture",
  },
  {
    percentage: 25,
    description: "The industry contributes to the GDP of Rwanda",
  },
  {
    percentage: 61,
    description:
      "Rwandan soil is suitable for agriculture as the soils are fertile",
  },
];

const Home = () => {
  return (
    <div className="font-noto">
      <div className="relative">
        <div className="absolute z-10 text-white">
          <div className="px-10">
            <p className="text-2xl mt-24">
              Utilize advanced technology to make informed irrigation decisions
              that improve crop growth and conserve water resources.
            </p>

            <div className="flex justify-center flex-col items-center">
              <h1 className="text-4xl font-bold">
                Welcome to Smart Irrigation
              </h1>
              <Button className="border mt-10 px-5 py-3 flex rounded-full gap-3 items-center hover:text-blue-500 hover:bg-white">
                <NavLink to={"/about"}>Learn more</NavLink>
                <FontAwesomeIcon icon={faArrowRight} />
              </Button>
            </div>
          </div>
        </div>
        <div>
          <img
            src={irrigation}
            alt="crops inside the green house"
            className="w-full h-96 object-cover transition-all brightness-50"
          />
        </div>
        <div className="px-24 bg-gradient-to-r from-gray-300 from-50% to-dark-blue-500 to-90% flex py-10 flex-col justify-center items-center gap-10">
          <div className="">
            <h1 className="text-3xl font-semibold pb-3">
              Rwanda GDP from Agriculture
            </h1>
            <p>
              According to the National Institute of Statistics of Rwanda GDP
              from Agriculture in Rwanda decreased to 656 RWF Billion in the
              second quarter of 2024 from 657 RWF Billion in the first quarter
              of 2024. GDP from Agriculture in Rwanda averaged 462.81 RWF
              Billion from 2006 until 2024, reaching an all time high of 657.00
              RWF Billion in the first quarter of 2024 and a record low of
              268.00 RWF Billion in the first quarter of 2006.
            </p>
          </div>
          <div>
            <img src={graph2} alt="" />
          </div>
        </div>

        <div className="pt-14 px-24">
          <h1 className="text-2xl pb-3 font-semibold">
            Status of Agriculture in Rwanda
          </h1>
          <div className="flex flex-col gap-14 pb-14">
            <p>
              Over the past 29 years, Rwanda has achieved rapid economic growth
              and significant poverty reduction, with agriculture playing a
              central role. The sector, contributing 25% of the national GDP,
              has grown by an average of 5% annually over 15 years. GDP per
              capita rose from $441 in 2007 to $1,004 in 2022. The Girinka
              program, initiated in 2006, added over 450,000 cows, boosting the
              cattle population to 1.5 million in 2022. This has improved
              livelihoods, nutrition, incomes, and social cohesion, with milk
              production increasing from 142,511 MT in 2005 to 999,976 MT in
              2022.
            </p>
            <div className="grid grid-cols-3 gap-8">
              {structureDetails.map((detail, index) => (
                <span
                  key={index}
                  className="flex flex-col items-center gap-10 shadow-lg shadow-gray-300 p-6 rounded-lg"
                >
                  <span className="bg-blue-500 p-12 rounded-full text-2xl font-bold text-white">
                    {detail.percentage}%+
                  </span>
                  <p>{detail.description}</p>
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Home;
