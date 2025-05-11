import { useRef, useState, useEffect } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import MarkdownPreview from '@uiw/react-markdown-preview';
import { Card } from "@/components/ui/card";
import { Loader2, Download, ThumbsUp } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ThemeToggle } from "@/components/theme-toggle";
import { Input } from "@/components/ui/input";
import { useTheme } from "@/components/theme-provider";
import { API_BASE_URL, API_ENDPOINTS, DEFAULT_VALUES } from "./constants";


interface SOWFormData {
  projectObjectives: string;
  projectScope: string;
  servicesDescription: string;
  specificFeatures: string;
  platformsTechnologies: string;
  integrations: string;
  designSpecifications: string;
  outOfScope: string;
  deliverables: string;
  timeline: string;
}

const SOWGenerator = () => {
  const [formData, setFormData] = useState<SOWFormData>(DEFAULT_VALUES || {
    projectObjectives: "",
    projectScope: "",
    servicesDescription: "",
    specificFeatures: "",
    platformsTechnologies: "",
    integrations: "",
    designSpecifications: "",
    outOfScope: "",
    deliverables: "",
    timeline: "",
  });
  const { theme } = useTheme();
  const [isGenerating, setIsGenerating] = useState(false);
  const [isLikeLoading, setIsLikeLoading] = useState(false);
  const [isChaGenerating, setIsChaGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState("");
  const { toast } = useToast();
  const [chatMessages, setChatMessages] = useState<{role: 'user' | 'assistant', content: string}[]>([]);
  const [chatInput, setChatInput] = useState("");
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages]);

  const handleChange = (field: keyof SOWFormData) => (
    e: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: e.target.value,
    }));
  };

  const handleDownloadDocx = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.GENERATED_SOW_PDF, {
        responseType: 'blob', // very important to receive binary data
      });
  
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
  
      // Create a local URL and download link (if you want to prompt user to download)
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'Generated_SOW_final.docx'); // filename
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to download DOCX file",
        variant: "destructive",
      });
      console.error(error);
    }
  }; 

  const handleGenerate = async () => {
    if (!formData.projectObjectives.trim()) {
      toast({
        title: "Error",
        description: "Project Objectives is required",
        variant: "destructive",
      });
      return;
    }
    setIsGenerating(true);

    try {
      const response = await axios.post(API_ENDPOINTS.GENERATE_SOW, formData, {
        headers: {
          'Content-Type': 'application/json',
        },    
      });

      if (response.status === 200) {
        setGeneratedContent(response.data.message)
        toast({
          title: "Success",
          description: "SOW has been generated",
        });
      }
      setIsGenerating(false);
    } catch (error) {
      setIsGenerating(false);
      toast({
        title: "Error",
        description: error?.message || 'Some error occurred while generating SOW',
        variant: "destructive",
      });
    }
  };

  const handleLikeSOW = async () => {
    setIsLikeLoading(true);
    try {
      const response = await axios.post(API_ENDPOINTS.LIKE_SOW, {
        content: generatedContent,
      });

      if (response.status === 200) {
        toast({
          title: "Success",
          description: "SOW liked successfully",
        });
      }
      setIsLikeLoading(false);
    } catch (error) {
      setIsLikeLoading(false);
      toast({
        title: "Error",
        description: error?.message || 'Some error occurred while liking SOW',
        variant: "destructive",
      });
    }
  };

  const handleSendMessage = () => {
    setIsGenerating(true);
    setIsChaGenerating(true);
    if (!chatInput.trim()) return;
    const userMsg = { role: 'user' as const, content: chatInput };
    setChatMessages((prev) => [...prev, userMsg]);
    setChatInput("");
    // Send message to backend
    axios.post(API_ENDPOINTS.CHAT, {
      message: chatInput,
      context: generatedContent,
    })
    .then((response) => {
      setGeneratedContent(response.data.message);
      setIsChaGenerating(false);
      setIsGenerating(false);
    }
    )
    .catch((error) => {
      setIsGenerating(false);
      setIsChaGenerating(false);
      toast({
        title: "Error",
        description: error?.message || 'Some error occurred while sending message',
        variant: "destructive",
      });
    }
    );
  };

  return (
    <ResizablePanelGroup direction="horizontal" className="min-h-[600px]">
      <ResizablePanel defaultSize={30} minSize={20}>
        <ScrollArea className="h-full">
          <div className="p-6 space-y-6">
            <div className="space-y-2">
              <Label htmlFor="projectObjectives" className="text-base font-semibold">
                Project Objectives <span className="text-red-500">*</span>
              </Label>
              <Textarea
                id="projectObjectives"
                placeholder="Enter the main objectives of the project..."
                value={formData.projectObjectives}
                onChange={handleChange("projectObjectives")}
                className="min-h-[100px]"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="projectScope" className="text-base">Project Scope</Label>
              <Textarea
                id="projectScope"
                placeholder="Define the scope of the project..."
                value={formData.projectScope}
                onChange={handleChange("projectScope")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="servicesDescription" className="text-base">
                Detailed Description of Services
              </Label>
              <Textarea
                id="servicesDescription"
                placeholder="Describe the services to be provided..."
                value={formData.servicesDescription}
                onChange={handleChange("servicesDescription")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="specificFeatures" className="text-base">
                Specific Features
              </Label>
              <Textarea
                id="specificFeatures"
                placeholder="List specific features if applicable..."
                value={formData.specificFeatures}
                onChange={handleChange("specificFeatures")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="platformsTechnologies" className="text-base">
                Platforms and Technologies
              </Label>
              <Textarea
                id="platformsTechnologies"
                placeholder="Specify platforms and technologies to be used..."
                value={formData.platformsTechnologies}
                onChange={handleChange("platformsTechnologies")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="integrations" className="text-base">Integrations</Label>
              <Textarea
                id="integrations"
                placeholder="List required integrations..."
                value={formData.integrations}
                onChange={handleChange("integrations")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="designSpecifications" className="text-base">
                Design Specifications
              </Label>
              <Textarea
                id="designSpecifications"
                placeholder="Enter design specifications if applicable..."
                value={formData.designSpecifications}
                onChange={handleChange("designSpecifications")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="outOfScope" className="text-base">Out of Scope</Label>
              <Textarea
                id="outOfScope"
                placeholder="Specify what is not included in the scope..."
                value={formData.outOfScope}
                onChange={handleChange("outOfScope")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="deliverables" className="text-base">Deliverables</Label>
              <Textarea
                id="deliverables"
                placeholder="List specific deliverables, quantities, and formats..."
                value={formData.deliverables}
                onChange={handleChange("deliverables")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="timeline" className="text-base">Project Timeline & Schedule</Label>
              <Textarea
                id="timeline"
                placeholder="Outline the project timeline and schedule..."
                value={formData.timeline}
                onChange={handleChange("timeline")}
                className="min-h-[100px]"
              />
            </div>

            <div className="sticky bottom-0 pb-4 pt-4 bg-background">
              <Button
                onClick={handleGenerate}
                disabled={isGenerating || !formData.projectObjectives.trim()}
                className="w-full mb-2"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generating
                  </>
                ) : (
                  "Generate"
                )}
              </Button>
            </div>
          </div>
        </ScrollArea>
      </ResizablePanel>

      <ResizableHandle withHandle />

      <ResizablePanel defaultSize={70}>
        <div className="p-6 h-full">
            <div className="space-y-4 h-full flex flex-col">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Statement Of Work</h3>
                <div className="flex items-center space-x-2">
                  {generatedContent && (
                    <>
                      <Button variant="outline" onClick={handleLikeSOW} disabled={isLikeLoading}>
                        {isLikeLoading ? (
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        ) : (
                          <ThumbsUp className="w-4 h-4" />
                        )}
                      </Button>
                    <Button variant="outline" onClick={handleDownloadDocx}>
                        <Download className="w-4 h-4 mr-2" />
                        Export to Word
                      </Button>
                    </>
                  )}
                  <ThemeToggle />
                </div>
              </div>
            <Card className="p-6 h-[calc(100%-15rem)] overflow-auto flex-1">
              <div className="prose max-w-none h-full">
                {(!generatedContent && !(isGenerating || isChaGenerating)) && (
                  <div className="flex items-center justify-center center h-full">
                    <p className="text-gray-500">Generate your SOW to see the preview here.</p>
                  </div>
                )}
                {(isGenerating || isChaGenerating) ? (
                  <div className="flex items-center justify-center center h-full">
                    <Loader2 className="w-6 h-6 animate-spin" />
                  </div>
                ) : (
                    <>
                     <div className="wmde-markdown-var" />
                      <MarkdownPreview
                        wrapperElement={{
                          "data-color-mode": theme === "dark" ? "dark" : "light",
                        }}
                        source={generatedContent}
                      />
                    </>
                )}
                </div>
              </Card>
              {/* Chat Interface */}
              {generatedContent && (
              <div className="mt-4 rounded-lg flex flex-col max-h-[10rem]">
                  <div className="flex-1 overflow-y-auto mb-2 space-y-2">
                    {chatMessages.map((msg, idx) => (
                      <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`rounded-lg px-3 py-2 max-w-[80%] text-sm ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-background border'}`}>
                          {msg.content}
                        </div>
                      </div>
                    ))}
                    <div ref={chatEndRef} />
                  </div>
                  <div className="flex gap-2">
                    <Input
                      type="text"
                      className="flex-1"
                      placeholder="Ask AI to refine your SOW..."
                      value={chatInput}
                      onChange={e => setChatInput(e.target.value)}
                      onKeyDown={e => { if (e.key === 'Enter') handleSendMessage(); }}
                      disabled={!generatedContent}
                    />
                    <Button
                      onClick={handleSendMessage}
                      disabled={isChaGenerating || !chatInput.trim() || !generatedContent}
                      size="sm">
                      {isChaGenerating ? 'Refining...' : 'Send'}
                    </Button>
                  </div>
                </div>
              )}
            </div>
        </div>
      </ResizablePanel>
    </ResizablePanelGroup>
  );
};

export default SOWGenerator;
