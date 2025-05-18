import { NavigationMenu, NavigationMenuItem, NavigationMenuList } from "@/components/ui/navigation-menu";
import SOWGenerator from "../features/SOWGenerator";
import { useTheme } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/theme-toggle";

const Index = () => {
  const { theme } = useTheme(); 
  return (
    <div className="min-h-screen bg-background animate-fade-in h-screen relative">
      <header className="flex h-[4rem] w-full shrink-0 items-center px-4 py-4 md:px-6 shadow-sm bg-background border-b  sticky top-0 z-50">
        <nav className="flex gap-6 justify-between items-center w-full">
          <div className="gap-2">
            <img src={theme === 'dark' ? '/letter-head-white.png' : '/letter-head.png'} className="h-8" />
            <p className="text-xs text-muted-foreground">
              Create Professional SOW in One Click
            </p>
          </div>
          <ThemeToggle />
        </nav>
      </header>
      <SOWGenerator />
    </div>
  );
};

export default Index;
