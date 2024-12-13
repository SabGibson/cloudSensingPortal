import { BlobServiceClient, ContainerClient, BlockBlobClient } from "@azure/storage-blob";
import { QueueServiceClient, QueueClient } from "@azure/storage-queue";
import { timeStamp } from "console";
import { source } from "puppeteer-core/internal/generated/injected.js";

interface ProducerClientConfig {
  blobConnectionString: string;
  queueConnectionString: string;
  blobContainerName: string;
  queueName: string;
}

interface QueueMessage {
  timestamp:number;
  source:string
  blobName:string;
}

export class ProducerClientManager {
  private blobClient: BlobServiceClient;
  private queueClient: QueueServiceClient;
  private containerClient: ContainerClient;
  private queueServiceClient: QueueClient;

  constructor(private readonly config: ProducerClientConfig) {
    this.validateConfig(config);
    this.config = config
    
    try {
      this.blobClient = BlobServiceClient.fromConnectionString(config.blobConnectionString);
      this.queueClient = QueueServiceClient.fromConnectionString(config.queueConnectionString);
      this.containerClient = this.blobClient.getContainerClient(config.blobContainerName);
      this.queueServiceClient = this.queueClient.getQueueClient(config.queueName);
    } catch (error) {
      throw new Error(`Failed to initialize storage clients: ${error.message}`);
    }
  }

  private validateConfig(config: ProducerClientConfig): void {
    if (!config.blobConnectionString) {
      throw new Error('Blob connection string is required');
    }
    if (!config.queueConnectionString) {
      throw new Error('Queue connection string is required');
    }
    if (!config.blobContainerName) {
      throw new Error('Blob container name is required');
    }
    if (!config.queueName) {
      throw new Error('Queue name is required');
    }
  }

  private async ensureContainerAndQueue(): Promise<void> {
    try {
      await Promise.all([
        this.containerClient.createIfNotExists(),
        this.queueServiceClient.createIfNotExists()
      ]);
    } catch (error) {
      throw new Error(`Failed to create container or queue: ${error.message}`);
    }
  }

  private generateBlobName(): string {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(7);
    return `${timestamp}-${random}.json`;
  }

  public async claimCheckCheckIn(rawData: string): Promise<{ blobUrl: string, blobName: string }> {
    if (!rawData) {
      throw new Error("Raw data is required!");
    }

    try {
      // Ensure container and queue exist
      await this.ensureContainerAndQueue();

      // Upload blob
      const blobName = this.generateBlobName();
      const blockBlobClient: BlockBlobClient = this.containerClient.getBlockBlobClient(blobName);
      await blockBlobClient.upload(rawData, Buffer.byteLength(rawData));

      // Send message to queue
      const blobUrl = blockBlobClient.url;
      const msg :QueueMessage = {timestamp:Date.now(), source:this.config.queueName,blobName:blobName }
      await this.queueServiceClient.sendMessage(
        JSON.stringify(msg)
      );

      return {
        blobUrl,
        blobName
      };

    } catch (error) {
      throw new Error(`Failed to process claim check: ${error.message}`);
    }
  }

  // Example usage of connection strings
  public static createFromEnvironment(): ProducerClientManager {
    const config: ProducerClientConfig = {
      blobConnectionString: process.env.AZURE_STORAGE_CONNECTION_STRING || '',
      queueConnectionString: process.env.AZURE_QUEUE_CONNECTION_STRING || '',
      blobContainerName: process.env.AZURE_BLOB_CONTAINER_NAME || 'default-container',
      queueName: process.env.AZURE_QUEUE_NAME || 'default-queue'
    };

    return new ProducerClientManager(config);
  }
}