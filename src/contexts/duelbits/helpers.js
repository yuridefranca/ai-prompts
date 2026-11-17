/**
 * Helper functions for PR Creator skill
 * These are reference implementations - adapt as needed for your AI workflow
 */

/**
 * Detects repository type from package.json or directory structure
 * @param {Object} workspace - Workspace information
 * @returns {string} 'frontend' | 'backend' | 'unknown'
 */
function detectRepositoryType(workspace) {
	// Check package.json name
	if (workspace.packageJson?.name) {
		const name = workspace.packageJson.name.toLowerCase();
		if (name.includes('frontend') || name.includes('fe')) {
			return 'frontend';
		}
		if (name.includes('backend') || name.includes('be')) {
			return 'backend';
		}
	}

	// Check directory structure
	const hasComponents = workspace.hasDirectory('src/components');
	const hasViews = workspace.hasDirectory('src/views');
	const hasControllers = workspace.hasDirectory('src/controllers');
	const hasServices = workspace.hasDirectory('src/services');

	if (hasComponents || hasViews) {
		return 'frontend';
	}
	if (hasControllers || hasServices) {
		return 'backend';
	}

	return 'unknown';
}

/**
 * Detects project from branch name
 * @param {string} branchName - Git branch name
 * @returns {string|null} 'multi-wallet' | 'world-cup-jackpot' | null
 */
function detectProject(branchName) {
	const lowerBranch = branchName.toLowerCase();

	// Multi Wallet patterns
	if (/mw-?\d*/i.test(branchName) || /multi-?wallet/i.test(branchName)) {
		return 'multi-wallet';
	}

	// World Cup Jackpot patterns
	if (/wcj-?\d*/i.test(branchName) || /world-?cup/i.test(branchName)) {
		return 'world-cup-jackpot';
	}

	return null;
}

/**
 * Extracts Jira ticket information from branch name
 * @param {string} branchName - Git branch name
 * @returns {Object|null} { category, number, fullTicket } or null
 */
function extractTicket(branchName) {
	// Match Jira ticket pattern at start of branch name
	const match = branchName.match(/(CORE|SUP|CAS|SPB|MW|WCJ)-(\d+)/i);

	if (match) {
		return {
			category: match[1].toUpperCase(),
			number: match[2],
			fullTicket: `${match[1].toUpperCase()}-${match[2]}`,
		};
	}

	return null;
}

/**
 * Determines base branch based on repository type and project
 * @param {string} repositoryType - 'frontend' | 'backend'
 * @param {string|null} project - Project name or null
 * @returns {string} Base branch name
 */
function determineBaseBranch(repositoryType, project) {
	const BASE_BRANCH_RULES = {
		'multi-wallet': {
			frontend: 'develop-multi-wallet-fe',
			backend: 'develop-multi-wallet-be',
		},
		'world-cup-jackpot': {
			frontend: 'develop-wcj-fe',
			backend: 'develop-wcj-be',
		},
		default: {
			frontend: 'develop',
			backend: 'develop',
		},
	};

	const projectKey = project || 'default';
	const rules = BASE_BRANCH_RULES[projectKey] || BASE_BRANCH_RULES['default'];

	return rules[repositoryType] || rules['frontend'] || 'develop';
}

/**
 * Generates PR title with proper format
 * @param {string} ticketNumber - Full ticket number (e.g., "MW-142")
 * @param {string|null} project - Project name or null
 * @param {string} title - PR title text
 * @returns {string} Formatted PR title
 */
function generatePRTitle(ticketNumber, project, title) {
	const projectAbbreviation = {
		'multi-wallet': '[MW1]',
		'world-cup-jackpot': '[WCJ]',
	};

	const parts = [`[${ticketNumber}]`];

	if (project && projectAbbreviation[project]) {
		parts.push(projectAbbreviation[project]);
	}

	parts.push(title);

	return parts.join(' ');
}

/**
 * Converts branch name to readable title
 * @param {string} branchName - Git branch name
 * @returns {string} Readable title
 */
function branchToTitle(branchName) {
	// Remove common prefixes and ticket numbers
	return branchName
		.replace(/^(feature|fix|bugfix|hotfix|chore)\//, '')
		.replace(/^(CORE|SUP|CAS|SPB|MW|WCJ)-\d+-/, '')
		.replace(/[-_]/g, ' ')
		.split(' ')
		.map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
		.join(' ');
}

// Export for use in AI workflow (conceptual)
module.exports = {
	detectRepositoryType,
	detectProject,
	extractTicket,
	determineBaseBranch,
	generatePRTitle,
	branchToTitle,
};
