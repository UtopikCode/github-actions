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
- `.github/workflows/openapi-publish.yml`
  - Reusable workflow to upload a generated OpenAPI JSON spec artifact from another job.
- `.github/actions/openapi-kiota`
  - Composite action to generate an OpenAPI document and create a Kiota client for C# or TypeScript.
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
      package-project: 'src/MyPackage/MyPackage.csproj'
      package-version: '1.0.0'
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
      overwrite: true
```

### Upload generated OpenAPI spec

```yaml
jobs:
  upload_openapi:
    uses: UtopikCode/github-actions/.github/workflows/openapi-publish.yml@main
    with:
      openapi-dll: 'src/MyApi/bin/Release/net10/MyApi.dll'
      openapi-output: 'openapi.json'
      openapi-upload-artifact: true
      openapi-upload-artifact-name: 'openapi-spec'
      openapi-temp-artifact: 'openapi-spec-temp'
```

This workflow is intended for use after another job generates an OpenAPI JSON file and uploads it as a temporary artifact.

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

### Publish a TypeScript client from a .NET API

```yaml
jobs:
  publish_npm:
    uses: UtopikCode/github-actions/.github/workflows/npm-publish.yml@main
    with:
      publish-npm: true
      package-dir: 'packages/my-ts-client'
      package-version: '1.0.0'
      npm-tag: 'latest'
      node-version: '20'
      registry: 'https://npm.pkg.github.com/'
      npm-auth-token: ${{ secrets.GITHUB_TOKEN }}
      openapi-project: 'src/MyApi/MyApi.csproj'
      openapi-dll: 'src/MyApi/bin/Release/net10/MyApi.dll'
      openapi-output: 'openapi.json'
      openapi-version: 'v1'
      kiota-output: 'packages/my-ts-client'
      kiota-namespace: 'MyApiClient'
      kiota-class-name: 'ApiClient'
      openapi-tool-version: '10.1.7'
      kiota-version: '1.31.1'
```

If `package-dir` is left as `'.'`, the workflow will publish from `kiota-output` when TypeScript client generation is enabled.

The publish directory must contain a `package.json` file. If Kiota output does not include a manifest, point `package-dir` to a folder with an existing npm package manifest or add one to the generated output before publishing.

For GitHub Packages, use the package scope that matches the repository owner/organization and ensure the publish token has access to that scope. If you want to republish the same version, set `overwrite: true`.

### Use the shared dotnet setup action

```yaml
steps:
  - uses: UtopikCode/github-actions/.github/actions/dotnet-setup@main
    with:
      dotnet-version: '10.0'
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Cleanup preview artifacts

Use the cleanup composite action in a workflow job to delete preview Docker and NuGet package versions when a pull request is closed.

```yaml
name: Cleanup preview artifacts
on:
  pull_request:
    types: [closed]

jobs:
  cleanup:
    uses: UtopikCode/github-actions/.github/workflows/cleanup-preview-artifacts.yml@main
    with:
      package-name: 'my-container-image'
      nuget-package: 'My.Package'
      npm-package: '@my-scope/my-package'
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

If you need a one-off step in an existing workflow, you can also use the composite action directly inside `steps:` as shown below:

```yaml
steps:
  - uses: UtopikCode/github-actions/.github/actions/cleanup-preview-artifacts@main
    with:
      package_name: 'my-container-image'
      nuget_package: 'My.Package'
      npm_package: '@my-scope/my-package'
      github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Notes

- The workflows are designed for GitHub Actions reusable workflow call (`workflow_call`).
- `.github/actions/dotnet-setup` configures GitHub Packages authentication for NuGet restore/publish.
- `docker-publish.yml` and `nuget-publish.yml` only run when their corresponding input flags are enabled.
- Adjust `dotnet-version` and input values to match your project requirements.
