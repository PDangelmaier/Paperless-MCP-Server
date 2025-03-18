declare namespace PaperlessMCP {
// Document related types
interface Document {
    id: string;
    title: string;
    content: string;
    fileType: FileType;
    fileSize: number;
    createdAt: Date;
    updatedAt: Date;
    tags: Tag[];
    metadata: DocumentMetadata;
    status: DocumentStatus;
    owner: User;
    permissions: DocumentPermission[];
    version: number;
    versionHistory: DocumentVersion[];
    isArchived: boolean;
    isDeleted: boolean;
}

interface DocumentMetadata {
    author?: string;
    description?: string;
    language?: string;
    pageCount?: number;
    customFields: Record<string, string | number | boolean>;
    ocr?: OCRData;
    source?: string;
    importance?: 'low' | 'medium' | 'high';
    expirationDate?: Date;
}

interface OCRData {
    text: string;
    confidence: number;
    languageDetected?: string;
    processedAt: Date;
}

interface DocumentVersion {
    id: string;
    versionNumber: number;
    createdAt: Date;
    createdBy: User;
    changes: string;
    documentId: string;
}

interface DocumentPermission {
    userId: string;
    accessLevel: AccessLevel;
    grantedAt: Date;
    grantedBy: string;
    expiresAt?: Date;
}

type DocumentStatus = 'draft' | 'review' | 'approved' | 'published' | 'archived';

type FileType = 'pdf' | 'docx' | 'xlsx' | 'pptx' | 'txt' | 'jpg' | 'png' | 'tiff' | 'other';

interface Tag {
    id: string;
    name: string;
    color?: string;
    category?: string;
}

// User related types
interface User {
    id: string;
    username: string;
    email: string;
    firstName?: string;
    lastName?: string;
    role: UserRole;
    createdAt: Date;
    updatedAt: Date;
    lastLogin?: Date;
    isActive: boolean;
    preferences: UserPreferences;
    permissions: Permission[];
    authenticationData: AuthenticationData;
}

interface UserPreferences {
    theme: 'light' | 'dark' | 'system';
    language: string;
    notificationSettings: NotificationSettings;
    defaultView: 'list' | 'grid' | 'details';
    itemsPerPage: number;
}

interface NotificationSettings {
    emailNotifications: boolean;
    pushNotifications: boolean;
    documentUpdates: boolean;
    systemNotifications: boolean;
    digestFrequency: 'daily' | 'weekly' | 'never';
}

interface AuthenticationData {
    passwordHash?: string;
    totpEnabled: boolean;
    totpSecret?: string;
    sessionTokens: SessionToken[];
    lastPasswordChange?: Date;
    passwordResetRequired: boolean;
    oauth?: OAuthConnection[];
}

interface SessionToken {
    token: string;
    createdAt: Date;
    expiresAt: Date;
    ipAddress?: string;
    userAgent?: string;
    isRevoked: boolean;
}

interface OAuthConnection {
    provider: 'google' | 'microsoft' | 'github';
    providerUserId: string;
    accessToken: string;
    refreshToken?: string;
    tokenExpiresAt: Date;
    connectedAt: Date;
}

type UserRole = 'admin' | 'manager' | 'editor' | 'viewer' | 'guest';

type AccessLevel = 'owner' | 'editor' | 'commenter' | 'viewer' | 'none';

interface Permission {
    resource: string;
    action: 'create' | 'read' | 'update' | 'delete' | 'manage';
}

// Configuration types
interface SystemConfiguration {
    version: string;
    maxFileSize: number;
    allowedFileTypes: FileType[];
    storagePath: string;
    tempPath: string;
    backupSettings: BackupSettings;
    securitySettings: SecuritySettings;
    ocrSettings: OCRSettings;
    emailSettings: EmailSettings;
    integrations: IntegrationSettings;
}

interface BackupSettings {
    enabled: boolean;
    schedule: 'daily' | 'weekly' | 'monthly';
    keepBackups: number;
    backupPath: string;
    includeFiles: boolean;
    includeDatabase: boolean;
    lastBackupDate?: Date;
}

interface SecuritySettings {
    passwordPolicy: PasswordPolicy;
    sessionTimeout: number;
    allowedIPs?: string[];
    enforceSSL: boolean;
    cors: CORSSettings;
    rateLimiting: RateLimitSettings;
}

interface PasswordPolicy {
    minLength: number;
    requireUppercase: boolean;
    requireLowercase: boolean;
    requireNumbers: boolean;
    requireSpecialChars: boolean;
    preventCommonPasswords: boolean;
    passwordExpiryDays: number;
    historyCount: number;
}

interface CORSSettings {
    allowedOrigins: string[];
    allowCredentials: boolean;
    maxAge: number;
}

interface RateLimitSettings {
    enabled: boolean;
    maxRequests: number;
    timeWindow: number;
    ipBased: boolean;
}

interface OCRSettings {
    enabled: boolean;
    defaultLanguage: string;
    enabledLanguages: string[];
    engineType: 'tesseract' | 'google' | 'azure' | 'custom';
    engineConfig: Record<string, any>;
    processAutomatically: boolean;
    minimumConfidence: number;
}

interface EmailSettings {
    smtpServer: string;
    smtpPort: number;
    useTLS: boolean;
    username?: string;
    password?: string;
    fromAddress: string;
    fromName: string;
    templates: Record<string, EmailTemplate>;
}

interface EmailTemplate {
    subject: string;
    body: string;
    isHTML: boolean;
}

interface IntegrationSettings {
    googleDrive?: OAuthServiceConfig;
    oneDrive?: OAuthServiceConfig;
    dropbox?: OAuthServiceConfig;
    slack?: WebhookConfig;
    customWebhooks: WebhookConfig[];
}

interface OAuthServiceConfig {
    enabled: boolean;
    clientId: string;
    clientSecret: string;
    redirectUri: string;
    scopes: string[];
}

interface WebhookConfig {
    enabled: boolean;
    url: string;
    events: string[];
    secret?: string;
    headers?: Record<string, string>;
}

// Search related types
interface SearchQuery {
    term?: string;
    filters: SearchFilter[];
    sort?: SearchSort;
    page: number;
    limit: number;
    includeArchived: boolean;
    includeDeleted: boolean;
    dateRange?: DateRange;
}

interface SearchFilter {
    field: string;
    operator: 'eq' | 'neq' | 'gt' | 'gte' | 'lt' | 'lte' | 'contains' | 'in' | 'nin';
    value: any;
}

interface SearchSort {
    field: string;
    direction: 'asc' | 'desc';
}

interface DateRange {
    from?: Date;
    to?: Date;
}

interface SearchResult<T> {
    items: T[];
    totalItems: number;
    page: number;
    totalPages: number;
    limit: number;
    executionTimeMs: number;
}

// API Response types
interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: ApiError;
    meta?: {
    timestamp: Date;
    requestId: string;
    version: string;
    };
}

interface ApiError {
    code: string;
    message: string;
    details?: any;
    stack?: string;
}

// Workflow and processing types
interface DocumentProcessor {
    id: string;
    name: string;
    description?: string;
    processorType: 'ocr' | 'classification' | 'extraction' | 'transformation' | 'validation';
    configuration: Record<string, any>;
    isEnabled: boolean;
    order: number;
    triggers: ProcessorTrigger[];
}

type ProcessorTrigger = 
    | { type: 'fileUpload', fileTypes?: FileType[] }
    | { type: 'schedule', cronExpression: string }
    | { type: 'documentChanged', fields: string[] };

interface WorkflowDefinition {
    id: string;
    name: string;
    description?: string;
    steps: WorkflowStep[];
    isEnabled: boolean;
    createdAt: Date;
    updatedAt: Date;
    createdBy: string;
}

interface WorkflowStep {
    id: string;
    name: string;
    type: 'processor' | 'approval' | 'notification' | 'integration' | 'custom';
    configuration: Record<string, any>;
    nextSteps: WorkflowTransition[];
}

interface WorkflowTransition {
    toStepId: string;
    condition?: string;
    priority: number;
}

interface WorkflowExecution {
    id: string;
    workflowId: string;
    documentId: string;
    status: 'running' | 'completed' | 'failed' | 'cancelled';
    startedAt: Date;
    completedAt?: Date;
    currentStepId?: string;
    stepResults: Record<string, StepExecutionResult>;
    variables: Record<string, any>;
}

interface StepExecutionResult {
    status: 'success' | 'failure' | 'skipped';
    startedAt: Date;
    completedAt: Date;
    output?: any;
    error?: string;
    nextStepId?: string;
}
}

