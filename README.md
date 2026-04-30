# github-actions

A reusable GitHub Actions repository for .NET, Docker, NuGet, and preview cleanup workflows.

## What’s included

- `.github/workflows/dotnet-build.yml`
  - Reusable .NET build workflow for restore and build of a solution/project.
- `.github/workflows/dotnet-codeql.yml`
  - Reusable CI workflow for static analysis, format checks, and CodeQL.
- `.github/workflows/docker-publish.yml`
  - Reusable Docker build + publish workflow for GHCR images.
- `.github/workflows/nuget-publish.yml`
  - Reusable NuGet package publish workflow with optional OpenAPI/Kiota generation.
- `.github/workflows/npm-publish.yml`
  - Reusable npm package publish workflow for TypeScript/JavaScript packages.
- `.github/actions/dotnet-setup`
  - Composite action to install .NET and configure GitHub Packages authentication.
- `.github/actions/cleanup-preview-artifacts`
  - Composite action to delete preview Docker and NuGet package versions when a PR closes.

## Usage

### Call a reusable workflow in this repo

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    uses: ./.github/workflows/dotnet-build.yml
    with:
      solution: 'src/MySolution.sln'
      dotnet-version: '10.0'
```

### Call a reusable workflow from another repository

```yaml
jobs:
  build:
    uses: UtopikCode/github-actions/.github/workflows/dotnet-build.yml@main
    with:
      solution: 'src/MySolution.sln'
      dotnet-version: '10.0'
```

### Publish Docker images

```yaml
jobs:
  publish:
    uses: UtopikCode/github-actions/.github/workflows/docker-publish.yml@main
    with:
      publish-docker: true
      docker-tags: 'ghcr.io/${{ github.repository_owner }}/myimage:latest'
```

### Publish NuGet packages

```yaml
jobs:
  publish_nuget:
    uses: UtopikCode/github-actions/.github/workflows/nuget-publish.yml@main
    with:
      publish-nuget: true
      nuget-project: 'src/MyPackage/MyPackage.csproj'
      nuget-package-version: '1.0.0'
      dotnet-version: '10.0'
```

### Publish npm packages

```yaml
jobs:
  publish_npm:
    uses: UtopikCode/github-actions/.github/workflows/npm-publish.yml@main
    with:
      publish-npm: true
      package-dir: 'packages/my-ts-package'
      package-version: '1.0.0'
      npm-tag: 'latest'
      node-version: '20'
      registry: 'https://npm.pkg.github.com/'
      npm-auth-token: ${{ secrets.GITHUB_TOKEN }}
```

For npmjs.org, pass a registry URL and an npm token instead:

```yaml
jobs:
  publish_npm:
    uses: UtopikCode/github-actions/.github/workflows/npm-publish.yml@main
    with:
      publish-npm: true
      package-dir: 'packages/my-ts-package'
      package-version: '1.0.0'
      npm-tag: 'latest'
      node-version: '20'
      registry: 'https://registry.npmjs.org/'
      npm-auth-token: ${{ secrets.NPM_TOKEN }}
```

### Use the shared dotnet setup action

```yaml
steps:
  - uses: UtopikCode/github-actions/.github/actions/dotnet-setup@main
    with:
      dotnet-version: '10.0'
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Cleanup preview artifacts

```yaml
steps:
  - uses: UtopikCode/github-actions/.github/actions/cleanup-preview-artifacts@main
    with:
      package_name: 'my-container-image'
      nuget_package: 'My.Package'
      github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Notes

- The workflows are designed for GitHub Actions reusable workflow call (`workflow_call`).
- `.github/actions/dotnet-setup` configures GitHub Packages authentication for NuGet restore/publish.
- `docker-publish.yml` and `nuget-publish.yml` only run when their corresponding input flags are enabled.
- Adjust `dotnet-version` and input values to match your project requirements.
