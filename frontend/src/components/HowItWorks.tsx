import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { MedalIcon, MapIcon, PlaneIcon } from "../components/Icons";

interface FeatureProps {
  icon: JSX.Element;
  title: string;
  description: string;
}

const features: FeatureProps[] = [
  {
    icon: <MedalIcon />,
    title: "Metadata Verification",
    description:    "Instantly identifies anomalies and discrepancies, ensuring metadata accuracy and compliance.",  },
  {
    icon: <MapIcon />,
    title: "Automated Metadata Correction",
    description:
      "Offers suggested metadata corrections based on processed PDF files, facilitating swift and accurate adjustments.",
  },
  {
    icon: <PlaneIcon />,
    title: "Question Answering Retriever",
    description:
      "Utilizes Vectara vector store technology for efficient retrieval of relevant information.",
  },
];

export const HowItWorks = () => {
  return (
    <section
      id="howItWorks"
      className="container text-center py-22 sm:py-30"
    >
      <h2 className="text-3xl md:text-4xl font-bold ">
        Fast and Accurate{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          Document Meta Data{" "}
        </span>
       Verification
      </h2>
      <p className="md:w-3/4 mx-auto mt-4 mb-8 text-xl text-muted-foreground">
        
Introducing DocVerifyRAG, your ultimate solution for hassle-free document verification! Say goodbye to errors and inefficiencies with our cutting-edge app. Powered by AI and Vectara vector store technology, we ensure metadata accuracy seamlessly. With DocVerifyRAG, breeze through verification, boost efficiency, and stay compliant effortlessly.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map(({ icon, title, description }: FeatureProps) => (
          <Card
            key={title}
            className="bg-muted/50"
          >
            <CardHeader>
              <CardTitle className="grid gap-4 place-items-center">
                {icon}
                {title}
              </CardTitle>
            </CardHeader>
            <CardContent>{description}</CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
};
