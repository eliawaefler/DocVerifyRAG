import { Badge } from "./ui/badge"; 
import {
  Card,
  CardTitle,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";

interface FeatureProps {
  title: string;
}

const features: FeatureProps[] = [
  {
    title: "UPLOAD DOCUMENT",
  },
];

const featureList: string[] = [
  "STEP1: Do this",
  "STEP2: Do that that",
  "STEP3: Do that that that",
  "STEP4: Do that that that that",
];

export const Features = () => {
  return (
    <section
      id="features"
      className="container py-28 sm:py-36 space-y-8"
    >
      <h2 className="text-3xl lg:text-4xl font-bold md:text-center">
        Get Started{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
           NOW{" "}
        </span>
	  Upload Your Document
      </h2>

      <div className="flex flex-wrap md:justify-center gap-4">
        {featureList.map((feature: string) => (
          <div key={feature}>
            <Badge
              variant="secondary"
              className="text-sm"
            >
              {feature}
            </Badge>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-1">
        {features.map(({ title }: FeatureProps) => (
          <Card key={title}>
	   <CardHeader className="text-3xl lg:text-4xl font-bold md:text-center">
              <CardTitle>{title}</CardTitle>
            </CardHeader>
            <CardFooter className="flex flex-wrap md:justify-center gap-4">
              <iframe
	src="https://salgadev-docverifyrag.hf.space"
	width="850"
style={{ border: 'none' }}
	height="750"
></iframe>

            </CardFooter>
          </Card>
        ))}
      </div>
    </section>
  );
};
