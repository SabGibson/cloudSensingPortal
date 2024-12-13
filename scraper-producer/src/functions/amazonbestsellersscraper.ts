import { app, InvocationContext, Timer } from "@azure/functions";
import { getDataFromWebMinerBot } from "../utilities/scraperbot";
import { MinerBotConfig } from "../types/scraperbot";
import {
  amazonJPMinePlan,
  amazonUkMinePlan,
  amazonUSMinePlan,
} from "../utilities/helpers/amazonmineplans";

const ukConfig: MinerBotConfig = {
  webSocketConfig: process.env.BROWSERWSCONFIG,
  blobConnectionString: process.env.BLOBCONNECTIONSTORAGE,
  blobContainerName: process.env.BLOBCONTAINERNAME,
  queueConnectionString: process.env.BLOBCONNECTIONSTORAGE,
  queueName: "amazonuk-queue",
  pageUrl: "https://www.amazon.co.uk/Best-Sellers/zgbs",
  customMinePlanFnc: amazonUkMinePlan,
};

const usConfig: MinerBotConfig = {
  webSocketConfig: process.env.BROWSERWSCONFIG,
  blobConnectionString: process.env.BLOBCONNECTIONSTORAGE,
  blobContainerName: process.env.BLOBCONTAINERNAME,
  queueConnectionString: process.env.BLOBCONNECTIONSTORAGE,
  queueName: "amazonus-queue",
  pageUrl: "https://www.amazon.com/Best-Sellers/zgbs",
  customMinePlanFnc: amazonUSMinePlan,
};

const jpConfig: MinerBotConfig = {
  webSocketConfig: process.env.BROWSERWSCONFIG,
  blobConnectionString: process.env.BLOBCONNECTIONSTORAGE,
  blobContainerName: process.env.BLOBCONTAINERNAME,
  queueConnectionString: process.env.BLOBCONNECTIONSTORAGE,
  queueName: "amazonjp-queue",
  pageUrl: "https://www.amazon.co.jp/-/en/gp/bestsellers",
  customMinePlanFnc: amazonJPMinePlan,
};

export async function amazonBestSellersScraperUK(
  myTimer: Timer,
  context: InvocationContext
): Promise<void> {
  await getDataFromWebMinerBot({...ukConfig,context:context});
  context.log("success: 0uk");
}

export async function amazonBestSellersScraperUS(
  myTimer: Timer,
  context: InvocationContext
): Promise<void> {
  await getDataFromWebMinerBot({...usConfig,context:context});
  context.log("success: 0us");
}

export async function amazonBestSellersScraperJP(
  myTimer: Timer,
  context: InvocationContext
): Promise<void> {
  await getDataFromWebMinerBot({...jpConfig,context:context});
  context.log("success: 0jp");
}

app.timer("amazonBestSellersScraperUK", {
  schedule: "0 0 * * * *",
  handler: amazonBestSellersScraperUK,
});

app.timer("amazonBestSellersScraperUS", {
  schedule: "0 0 * * * *",
  handler: amazonBestSellersScraperUS,
});

app.timer("amazonBestSellersScraperJP", {
  schedule: "0 0 * * * *",
  handler: amazonBestSellersScraperJP,
});
