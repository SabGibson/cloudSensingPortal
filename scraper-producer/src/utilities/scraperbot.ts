import { MinerBotConfig } from "../types/scraperbot";
import puppeteer, { Browser } from "puppeteer-core";
import { ProducerClientManager } from "./helpers/claimcheckhelper";

export async function getDataFromWebMinerBot(
  args: MinerBotConfig
): Promise<void> {
  let browser: Browser ;
  let producerClientManager : ProducerClientManager
  let context = args.context? args.context : null;
  try {
    // init putteteer connection
    browser = await puppeteer.connect({
      browserWSEndpoint: args.webSocketConfig,
    });

    context.log("Will attempt to configure producer client")
    //init eventhub connection
    producerClientManager = new ProducerClientManager({
      blobConnectionString: args.blobConnectionString,
      queueConnectionString: args.queueConnectionString,
      blobContainerName: args.blobContainerName,
      queueName: args.queueName
    });
    context.log("producer client configured")
    // navigate to page and config browser
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(3 * 60 * 1000);
    await page.goto(`${args.pageUrl}`);


    // ## mining logic 
    const content = await args.customMinePlanFnc(page);
    context.log("defined message")

    context.log("attempt to publish message message")
    //publish to azure eventhub
    await producerClientManager.claimCheckCheckIn(content)
    context.log("message published")


  } catch (err) {
    context.error("ERROR", err);
  } finally {
    browser?.close();
    
  }
}
