import { InvocationContext } from "@azure/functions";
import { Page } from "puppeteer-core";

export  type MinePlanFnc = (page:Page) => Promise<string>;

export type MinerBotConfig = {
  webSocketConfig: string;
  blobConnectionString: string;
  blobContainerName:string;
  queueConnectionString: string;
  queueName:string;
  pageUrl: string;
  customMinePlanFnc: MinePlanFnc;
  context?:InvocationContext
};
