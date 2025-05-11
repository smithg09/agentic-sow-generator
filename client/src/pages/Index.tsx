import { NavigationMenu, NavigationMenuItem, NavigationMenuList } from "@/components/ui/navigation-menu";
import SOWGenerator from "../features/SOWGenerator";

const Index = () => {

  return (
    <div className="min-h-screen bg-background animate-fade-in h-screen relative">
      <SOWGenerator />
    </div>
  );
};

export default Index;
