import { Page } from "puppeteer-core"
import { MinePlanFnc } from "../../types/scraperbot"

export const amazonUkMinePlan:MinePlanFnc = async (page:Page) =>{
    const selector = '.a-carousel' // #CardInstancew-vtCis4km4OA1dlVxQ6jQ > div > div > div
    
    await page.waitForSelector(selector) 
    const content = await page.$(selector);
    const textHtml = await content.evaluate(element => element.innerHTML);
    return textHtml
}

export const amazonUSMinePlan:MinePlanFnc = async (page:Page) =>{
    const selector = '.a-carousel' //'#CardInstance98_pYSQCWgF-yB0tuAKmMA > div > div > div' // '.a-carousel'
    await page.waitForSelector(selector) 
    const content = await page.$(selector);
    const textHtml = await content.evaluate(element => element.innerHTML);
    return textHtml

}

export const amazonJPMinePlan:MinePlanFnc = async (page:Page) =>{
    const selector = '.a-carousel' // '#CardInstancefVl5rHynuVcTydoN_encoA > div > div > div' // 
    await page.waitForSelector(selector) 
    const content = await page.$(selector);
    const textHtml = await content.evaluate(element => element.innerHTML);
    return textHtml

}

